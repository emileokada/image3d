from __future__ import division
import math

def pad_left(l,k):
    return l[-k:] + l

def pad_right(l,k):
    return l + l[:k]

def transpose(l):
    return zip(*l)

def binomial(n,k):
    return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def binomial_density(n):
    return [binomial(n,k)/(2**n) for k in range(n+1)]

def dot_product(lista,listb):
    return sum(a*b for a,b in zip(lista,listb))

def differentiate(y, step_size):
    y_temp = y[-1:] + y + y[:1]
    return [(t - s)/(2*step_size) for s, t in zip(y_temp, y_temp[2:])]

def list_convolve(l,kernel):
    left = (len(kernel)-1)//2
    right = len(kernel)//2
    l_temp = l
    if left > 0:
        l_temp = l[-left:] + l + l[:right]
    elif right > 0:
        l_temp = l + l[:right]
    if kernel != []:
        return [dot_product(l_temp[i:i+len(kernel)],kernel) for i in range(len(l_temp)-len(kernel)+1)]
    return l
