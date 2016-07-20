from PIL import Image
import os, sys

files = ['./pictures/'+f for f in os.listdir('./pictures/')]

for f in files:
    im = Image.open(f)
    s = im.size
    out = im.crop((0,0,s[0]-4,s[1]-4))
    out.save(f,'JPEG')

