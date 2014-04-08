
# coding: utf-8

# In[3]:

import os

from PIL import Image, ImageFont
from PIL.ImageDraw import Draw


# In[4]:

PALEYELLOW = '#FBFFD9'
BLACK      = '#000000'
GRAY       = '#303030'


# In[5]:

chars = [chr(x) for x in range(48, 122)]
[chars.append(' ') for x in range(8)] # pad to 49

gridsize = 10

lettergrid = [chars[(i*gridsize)+0:(i*gridsize)+gridsize] for i in range(gridsize-1)]
lettergrid


# In[6]:

imagewidth = 1080
imageheight = 720
fontsize = 60
fontpath = r".\fonts\JosefinSans-Regular.ttf"
fgcolor = GRAY # GRAY or PALEYELLOW
bgcolor = BLACK


# In[7]:

assert os.path.exists(fontpath)
font = ImageFont.truetype(size=fontsize,filename=fontpath)

img = Image.new("RGBA", (imagewidth, imageheight))
draw = Draw(img)
draw.rectangle(((0,0), (imagewidth, imageheight)), fill=bgcolor)

cellwidth = imagewidth/len(lettergrid[0]) 
cellheight = imageheight/len(lettergrid) 

for ir,row in enumerate(lettergrid):
    for il,letter in enumerate(row):
        celly = ir*cellheight
        cellx = il*cellwidth
        
        # get the line size
        text_width,text_height = font.getsize(letter)
        text_off_x, text_off_y = font.getoffset(letter)
        
        # center letter in the grid
        x_pos = cellx + (cellwidth-text_width-text_off_x)/2 
        y_pos = celly + (cellheight-text_height-text_off_y)/2

        draw.text((x_pos, y_pos), letter, fill=fgcolor,font=font)

        



# In[8]:

img.save('./temp/unlit.jpg')


# In[ ]:



