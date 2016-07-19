from __future__ import division
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import math
import re
import os
from misc import *

class image3d:
    def __init__(self,files):
        (self.width, self.height) = Image.open(files[0]).size
        self.resolution = len(files)
        #self.aspect = self.width/self.height
        self.aspect = 1
        self.shadow_list = [[] for i in range(self.height)]
        self.x, self.y, self.z = [], [], []

        #Determine the shadow function
        for f in files:
            img = Image.open(f)
            img = self.preprocess(img)
            img_data = self.img_to_array(img)
            for i, row in enumerate(img_data):
                (first, last) = self.read_value(row)
                self.shadow_list[i].insert(len(self.shadow_list[i])//2,first)
                self.shadow_list[i].append(last)

        for i in range(self.height):
            #Smooth the data by convolving with discrete Gaussian (i.e. binomial distribution)
            self.shadow_list[i] = list_convolve(self.shadow_list[i],binomial_density(14))

            #Add points
            coords = transpose(self.convex_hull(i))
            self.x.append(coords[0])
            self.y.append(coords[1])
            self.z.append(coords[2])

        self.x = transpose(map(lambda column: list_convolve(column,binomial_density(4)),transpose(self.x)))
        self.y = transpose(map(lambda column: list_convolve(column,binomial_density(4)),transpose(self.y)))

        counter = 0
        for i in range(self.height):
            k = i - counter
            if sum(self.x[k]) == 0 and sum(self.y[k]) == 0:
                del self.x[k]
                del self.y[k]
                del self.z[k]
                counter = counter + 1

        #Create figure
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(self.flat_x,self.flat_y,self.flat_z,marker='.')
        plt.xlim([-90,90])
        plt.ylim([-90,90])
        plt.show()
        
    @property
    def flat_x(self):
        return [x_coord for row in self.x for x_coord in row]

    @property
    def flat_y(self):
        return [y_coord for row in self.y for y_coord in row]

    @property
    def flat_z(self):
        return [z_coord for row in self.z for z_coord in row]

    def preprocess(self,img):
        """Convert image to greyscale and binarize image"""

        img = img.convert('L')
        out = img.point(lambda i: 255 if i>255/2 else 0)
        return out

    def img_to_array(self,img):
        """Convert Image object to matrix"""

        l = list(img.getdata())
        (w,h) = img.size
        return [l[w*i:w*(i+1)] for i in range(h)]

    def read_value(self,img_row):
        """Find shadow function value for a particular row"""

        mid_point = len(img_row)//2
        try:
            first = mid_point - img_row.index(0)
        except ValueError:
            first = 0
        try:
            last = len(img_row) - 1 - img_row[::-1].index(0) - mid_point
        except ValueError:
            last = 0
        return (first, last)

    def convex_hull(self,z_coord):
        """Calculate the points belonging to the convex hull of the particular level set"""

        theta = np.linspace(0,2*math.pi,2*self.resolution)
        shadow_derivative = differentiate(self.shadow_list[z_coord], math.pi/self.resolution)
        return [(self.aspect*(h*math.cos(t)-s*math.sin(t)),self.aspect*(h*math.sin(t)+s*math.cos(t)),self.height-z_coord) for t, h, s in zip(theta,self.shadow_list[z_coord],shadow_derivative)]

files = ['./Pictures/'+f for f in os.listdir('./Pictures/')]
files = sorted(files, key=lambda x: int(re.search(r'(\d+)\.jpg',x).group(1)))

space_shuttle = image3d(files)
