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

class denoise3d:
    def __init__(self,mat):
        (self.depth, self.height, self.width) = mat.shape

        tau = 1/math.sqrt(8)
        sigma = 1/math.sqrt(8)
        theta = 1
        lam = 16
        gamma = 0.35*lam
        
        x = np.zeros([self.depth,self.height,self.width])
        x_bar = x

        y = np.zeros([3,self.depth,self.height,self.width])

        for i in range(10):
            print i
            q = y+sigma*self.grad(x_bar)
            denom = np.maximum(1,np.sqrt(q[0]**2+q[1]**2+q[2]**2))
            y[0] = q[0]/denom
            y[1] = q[1]/denom
            y[2] = q[2]/denom

            x_old = x
            x = (x+tau*self.div(y) + tau*lam*mat)/(1+tau*lam)

            theta = 1/np.sqrt(1+2*gamma*tau)
            tau = theta*tau
            sigma = sigma/theta

            x_bar = x + theta*(x-x_old)

        self.smoothed_matrix = x


    def grad(self,u):
        (d,h,w) = u.shape

        forward = [[[u[i+1][j][k]-u[i][j][k] if i < d-1 else 0 for k in range(w)] for j in range(h)] for i in range(d)]
        side = [[[u[i][j+1][k]-u[i][j][k] if j < h-1 else 0 for k in range(w)] for j in range(h)] for i in range(d)]
        up = [[[u[i][j][k+1]-u[i][j][k] if k < w-1 else 0 for k in range(w)] for j in range(h)] for i in range(d)]

        return np.array([forward, side, up])

    def div(self,p):
        (dim,d,h,w) = p.shape
        one = np.array([[[p[0,i,j,k]-p[0,i-1,j,k] if 0 < i < d-1 else p[0,i,j,k] if i == 0 else -p[0,i-1,j,k] for k in range(w)] for j in range(h)] for i in range(d)])
        two = np.array([[[p[1,i,j,k]-p[1,i,j-1,k] if 0 < j < h-1 else p[1,i,j,k] if j == 0 else -p[1,i,j-1,k] for k in range(w)] for j in range(h)] for i in range(d)])
        three = np.array([[[p[2,i,j,k]-p[2,i,j,k-1] if 0 < k < w-1 else p[2,i,j,k] if k == 0 else -p[2,i,j,k-1] for k in range(w)] for j in range(h)] for i in range(d)])
        return one+two+three
