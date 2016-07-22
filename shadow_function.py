from __future__ import division
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import math
import re
import os
from misc import *

class image3d:
    def __init__(self,files):
        (self.width, self.height) = Image.open(files[0]).size
        self.mid = self.width//2

        self.resolution = len(files)

        self.vertical_pixel_spacing = self.height//50
        self.xy_scaling = 5

        self.scaled_width = self.width//self.xy_scaling
        self.scaled_mid = self.scaled_width//2

        self.xy = self.scaled_mid*0.75
        self.aspect = 1

        self.shadow_list = [[] for i in range(self.height)]
        self.shadow_bands = [[] for i in range(self.height)]
        self.x, self.y, self.z = [], [], []

        #Determine the shadow function
        for f in files:
            img = Image.open(f)
            img = self.preprocess(img)
            img_data = self.img_to_array(img)
            for i, row in enumerate(img_data):
                if i % self.vertical_pixel_spacing == 0:
                    self.shadow_bands[i].append(self.read_bands(row))

        for i in range(self.height):
                if i % self.vertical_pixel_spacing == 0:
                    #Add points
                    #coords = self.get_coords(self.intersected_area(i),i)
                    coords = self.get_coords(self.morphological_perimeter(self.intersected_area(i)),i)
                    self.x.append(coords[0])
                    self.y.append(coords[1])
                    self.z.append(coords[2])

        self.sparse_x = self.x
        self.sparse_y = self.y
        self.sparse_z = self.z

        #Create figure
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(self.flat_x,self.flat_y,self.flat_z,marker='.')
        #collection = Poly3DCollection(self.polygon_vertices, linewidths=1, alpha=0.5)
        #collection.set_facecolor([0.5,0.5,1])
        #ax.add_collection3d(collection)
        plt.xlim([-self.xy,self.xy])
        plt.ylim([-self.xy,self.xy])
        plt.show()
        
    @property
    def flat_x(self):
        return [x_coord for row in self.sparse_x for x_coord in row]

    @property
    def flat_y(self):
        return [y_coord for row in self.sparse_y for y_coord in row]

    @property
    def flat_z(self):
        return [z_coord for row in self.sparse_z for z_coord in row]

    def preprocess(self,img):
        """Convert image to greyscale and binarize image"""

        img = img.convert('L')
        out = img.point(lambda i: 0 if i>255/2 else 1)
        return out

    def img_to_array(self,img):
        """Convert Image object to matrix"""

        l = list(img.getdata())
        (w,h) = img.size
        return [l[w*i:w*(i+1)] for i in range(h)]

    def read_bands(self,img_row):
        differences = [t-s for s,t in zip(img_row,img_row[1:])]
        left_edges = [i+1-self.mid for i,el in enumerate(differences) if el == 1]
        right_edges = [i-self.mid for i,el in enumerate(differences) if el == -1]

        if len(left_edges)>len(right_edges):
            right_edges.append(len(img_row)-1)
        elif len(left_edges)<len(right_edges):
            left_edges.append(0)

        if len(left_edges) == len(right_edges):
            return zip(left_edges, right_edges)
        return []

    def in_band(self, theta, m, n, bands):
        d = -(m-self.scaled_mid)*math.sin(theta)+(n-self.scaled_mid)*math.cos(theta)
        for lower, upper in bands:
            if lower <= self.xy_scaling*d <= upper:
                return True
        return False

    def banded_matrix(self,theta,bands):
        return np.array([[1 if self.in_band(theta,i,j,bands) else 0 for i in range(self.scaled_width)] for j in range(self.scaled_width)])

    def intersected_area(self,z_coord):
        print z_coord
        intersection = np.array([[1 for i in range(self.scaled_width)] for j in range(self.scaled_width)])
        for i, bands in enumerate(self.shadow_bands[z_coord]):
            intersection = intersection * self.banded_matrix(math.pi*i/self.resolution,bands)
        return intersection

    def get_coords(self,matrix,z_coord):
        xy = map(list,np.array(np.nonzero(matrix))-self.scaled_mid) 
        return xy + [[self.height-z_coord for i in range(len(xy[0]))]]
        
    def morphological_perimeter(self,matrix):
        perimeter_matrix = [[0 for i in range(self.scaled_width)] for j in range(self.scaled_width)]
        adj = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        for i in range(self.scaled_width):
            for j in range(self.scaled_width):
                if matrix[i][j] == 1:
                    for x,y in adj:
                        if 0 <= i-x < self.scaled_width and 0 <= j-y < self.scaled_width:
                            if matrix[i-x][j-y] == 0:
                                perimeter_matrix[i][j] = 1
                    
        return perimeter_matrix 




files = ['./pictures/'+f for f in os.listdir('./pictures/')]
files = sorted(files, key=lambda x: int(re.search(r'(\d+)\.jpg',x).group(1)))

space_shuttle = image3d(files)
