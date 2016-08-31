from __future__ import division
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as cm
from meshpy.tet import MeshInfo, build

import math
import re
import os
from misc import *
from denoise3d import denoise3d

class image3d:
    def __init__(self,files):
        (self.width, self.height) = Image.open(files[0]).size
        self.mid = self.width//2

        self.resolution = len(files)

        self.vertical_pixel_spacing = self.height//30
        self.xy_scaling = 10

        self.scaled_width = self.width//self.xy_scaling
        self.scaled_mid = self.scaled_width//2

        self.xy = self.scaled_mid*0.75
        self.aspect = 1

        self.shadow_bands = [[] for i in range(self.height)]
        self.x, self.y, self.z = [], [], []
        self.mat = []

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
                    temp_mat = self.intersected_area(i)
                    #temp_mat = self.morphological_perimeter(self.intersected_area(i))
                    self.mat.append(temp_mat)
                    coords = self.get_coords(temp_mat,i)
                    #coords = self.get_coords(self.morphological_perimeter(self.intersected_area(i)),i)
                    self.x.append(coords[0])
                    self.y.append(coords[1])
                    self.z.append(coords[2])

        self.mat = np.array(self.mat)

        self.sparse_x = self.x
        self.sparse_y = self.y
        self.sparse_z = self.z

        """
        #Create figure
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(self.flat_x,self.flat_y,self.flat_z,marker='.')
        plt.xlim([-self.xy,self.xy])
        plt.ylim([-self.xy,self.xy])
        plt.show()
        """
        
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
        print str(100*z_coord/self.height) + "%"
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

    def get_coordinates_and_density(self,matrix):
        (d,h,w) = matrix.shape
        nonzero = [[],[],[],[]]
        for i in range(d):
            for j in range(h):
                for k in range(w):
                    if matrix[i,j,k] > 0.5:
                        nonzero[0].append(j-self.scaled_mid)
                        nonzero[1].append(k-self.scaled_mid)
                        nonzero[2].append(self.height-i*self.vertical_pixel_spacing)
                        nonzero[3].append(1)
        return nonzero

    def matrix_to_plot(self,smooth_matrix):
        [x,y,z,density] = self.get_coordinates_and_density(smooth_matrix)
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(x,y,z,marker='.',c='r')
        #ax.scatter(self.flat_x,self.flat_y,self.flat_z,marker='.',c='b')
        #ax.plot_wireframe(self.flat_x,self.flat_y,self.flat_z)
        ax.plot_surface(self.flat_x,self.flat_y,self.flat_z)
        plt.xlim([-self.xy,self.xy])
        plt.ylim([-self.xy,self.xy])
        plt.show()

    def write_to_file(self,f):
        f = open(f,'w')
        f.write(str(self.flat_x)) 
        f.write(str(self.flat_y)) 
        f.write(str(self.flat_z)) 
        f.close()

    def mesh(self):
        mesh_info = MeshInfo()
        mesh_info.set_points(transpose([self.flat_x,self.flat_y,self.flat_z]))
        mesh = build(mesh_info)
        print 'yo'
        for i, t in enumerate(mesh.elements):
            print i, t


files = ['./pictures/'+f for f in os.listdir('./pictures/')]
files = sorted(files, key=lambda x: int(re.search(r'(\d+)\.jpg',x).group(1)))

space_shuttle = image3d(files)
space_shuttle.write_to_file('x.txt')
space_shuttle.mesh()

#space_shuttle.matrix_to_plot(space_shuttle.smoothed_surface.smoothed_matrix)
space_shuttle.matrix_to_plot(space_shuttle.mat)

