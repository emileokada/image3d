from __future__ import division
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import png

import math
import re
import os

class denoise:
    def __init__(self,f):
        self.im = Image.open(f)
        self.im = self.im.convert('L')
        (self.width, self.height) = self.im.size

        tau = 1/math.sqrt(8)
        sigma = 1/math.sqrt(8)
        theta = 1
        lam = 8
        gamma = 0.35*lam
        
        self.im_array = self.img_to_array(self.im)
        x = np.zeros([self.height,self.width])
        x_bar = x

        y = np.zeros([2,self.height,self.width])

        for i in range(30):
            q = y+sigma*self.grad(x_bar)
            denom = np.maximum(1,np.sqrt(q[0]**2+q[1]**2))
            y[0] = q[0]/denom
            y[1] = q[1]/denom

            x_old = x
            x = (x+tau*self.div(y) + tau*lam*self.im_array)/(1+tau*lam)

            theta = 1/np.sqrt(1+2*gamma*tau)
            tau = theta*tau
            sigma = sigma/theta

            x_bar = x + theta*(x-x_old)

        s = x*255
        f = open('denoised.png', 'wb')
        w = png.Writer(len(s[0]), len(s), greyscale=True, bitdepth=8)
        w.write(f, s)
        f.close()

    def img_to_array(self,img):
        """Convert Image object to matrix"""

        l = list(img.getdata())
        (w,h) = img.size
        return np.array([l[w*i:w*(i+1)] for i in range(h)])/255

    def grad(self,u):
        w = len(u[0])
        h = len(u)

        vertical = [[u[i+1][j]-u[i][j] for j in range(w)] for i in range(h-1)] + [[0 for j in range(w)]]
        horizontal = [[u[i][j+1]-u[i][j] if j < w -1 else 0 for j in range(w)] for i in range(h)]

        return np.array([vertical, horizontal])

    def div(self,p):
        (d,h,w) = p.shape
        one = np.array([[p[0,i,j]-p[0,i-1,j] if 0 < i < h-1 else p[0,i,j] if i == 0 else -p[0,i-1,j] for j in range(w)] for i in range(h)])
        two = np.array([[p[1,i,j]-p[1,i,j-1] if 0 < j < w-1 else p[1,i,j] if j == 0 else -p[1,i,j-1] for j in range(w)] for i in range(h)])
        return one+two

f = 'noisy2.png'

denoised_image = denoise(f)

