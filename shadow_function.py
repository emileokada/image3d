from __future__ import division
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt

import math
import re
import os

def differentiate(y, step_size):
    y_temp = y[-1:] + y + y[:1]
    return [(t - s)/(2*step_size) for s, t in zip(y_temp, y_temp[2:])]

class image3d:
    def __init__(self,files):
        (self.width, self.height) = Image.open(files[0]).size
        self.resolution = len(files)
        self.shadow_list = [[] for i in range(self.height)]

        for f in files:
            img = Image.open(f)
            img = self.preprocess(img)
            img_data = self.img_to_array(img)
            for i, row in enumerate(img_data):
                (first, last) = self.read_value(row)
                self.shadow_list[i].insert(len(self.shadow_list[i])//2,first)
                self.shadow_list[i].append(last)

    def preprocess(self,img):
        img = img.convert('L')
        out = img.point(lambda i: 255 if i>255/2 else 0)
        return out

    def img_to_array(self,img):
        l = list(img.getdata())
        (w,h) = img.size
        return [l[w*i:w*(i+1)] for i in range(h)]

    def read_value(self,img_row):
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
    def convex_hull(self,shadow_value):
        theta = np.linspace(0,2*math.pi,2*self.resolution)
        shadow_derivative = differentiate(shadow_value, math.pi/self.resolution)
        return [(h*math.cos(t)-s*math.sin(t),b*math.sin(t)+s*cos(t)) for t, h, s in zip(theta,shadow_value,shadow_derivate)]

files = ['./Pictures/'+f for f in os.listdir('./Pictures/')]
files = sorted(files, key=lambda x: int(re.search(r'(\d+)\.jpg',x).group(1)))

space_shuttle = image3d(files)
x = np.linspace(0,2*math.pi,2*80)
plt.plot(x,space_shuttle.shadow_list[100],'-',linewidth=2)
plt.plot(x,differentiate(space_shuttle.shadow_list[100],math.pi/80),'-',linewidth=1)
plt.show()
