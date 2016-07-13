from PIL import Image
import os, sys

files = ['./Pictures/'+f for f in os.listdir('./Pictures/')]

for f in files:
    im = Image.open(f)
    out = im.crop((0,0,210,430))
    out.save(f,'JPEG')

