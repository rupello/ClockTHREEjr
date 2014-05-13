
# coding: utf-8

# In[25]:

from PIL import Image, ImageFont
from PIL.ImageDraw import Draw

from string import lower,upper
import codecs
from numpy import array,arange


# In[26]:

PALEYELLOW = '#FBFFD9'
BLACK      = '#000000'
GRAY       = '#303030'


# In[27]:

def in2pxx(inches):
    return int(inches*pxpi_x)


# In[28]:

def in2pxy(inches):
    return int(inches*pxpi_y)


# In[29]:

def pt2pxx(pt):
    return in2pxx(pt/inch)


# In[30]:

def pt2pxy(pt):
    return in2pxy(pt/inch)


# In[31]:

def drawhole(draw,h,outline):
    x,y,rx,ry = (pt2pxx(h[0]),pt2pxy(h[1]),pt2pxx(h[2]),pt2pxy(h[2]))    
    bbox = (x-rx,y-ry,x+rx,y+ry)
    draw.ellipse(bbox,outline)    


# In[32]:

def drawletter(draw,pos,font,letter,fill):
    x,y = (pt2pxx(pos[0]),pt2pxy(pos[1]))    
    text_width,text_height = font.getsize(letter)
    text_off_x, text_off_y = font.getoffset(letter)   
    # center letter in the grid
    asc,desc = font.getmetrics()
    
    # adjust to center letter over the led
    x = x - (text_width/2 + text_off_x)
    y = y - (asc+desc)/2
        
    draw.text((x, y),letter , fill=fill,font=font)


# In[33]:

def drawleds(draw,led_xs,led_ys,outline):
    for i, y in enumerate(led_ys):
        for j, x in enumerate(led_xs):
            drawhole(draw,[x,y,5.],outline)                


# In[34]:

def drawletters(draw,lines,font,case,led_xs,led_ys,fill):
    for i, y in enumerate(led_ys):
        for j, x in enumerate(led_xs):
            drawletter(draw,(x,y),font,case(lines[i][j]),fill)


# In[35]:

def encodeLetters(style,case,encName='utf-8'):
    
    if type(style) == type(''):
        lines = style.strip().splitlines()
    else:
        lines = style

    decoder = codecs.lookup(encName)[1]
    
    def decodeFunc(txt):
        if txt is None:
            return ' '
        else:
            return case(decoder(txt, errors='replace')[0])
    
    def decodeFunc(txt):
        if txt is None:
            return ' '
        else:
            return txt
    
    return [[decodeFunc(case(char)) for char in line] for line in lines]


# In[49]:

def drawclock(fontpath,fontsize,fgcolor,bgcolor,style,case,drawLEDs=False):
    # init font
    scaledfontsize = pt2pxy(fontsize)
    font = ImageFont.truetype(size=scaledfontsize,filename=fontpath)
    lines = encodeLetters(style,case)

    img = Image.new("RGBA", (pt2pxx(WIDTH), pt2pxy(HEIGHT)))
    draw = Draw(img)
    draw.rectangle(((0,0), (pt2pxx(WIDTH),pt2pxy(HEIGHT))), fill=bgcolor)

    for h in corner_holes:
        drawhole(draw,h,fgcolor)

    if drawLEDs:
        drawleds(draw,led_xs,led_ys,fgcolor)
    
    drawletters(draw,lines,font,case,led_xs,led_ys,fgcolor)

    del draw
    return img


# In[79]:

# dimensions (in 1/72 inch points)
inch = 72.0
cm   = inch / 2.54
mm   = cm * 0.1
pica = 12.0

PCB_OFF = .05 * inch
HEIGHT = 9 * inch + 2 * PCB_OFF
WIDTH = 9 * inch + 2 * PCB_OFF
BEND_R = 10 * mm
# EDGE_THICKNESS = 3 * mm
EDGE_THICKNESS = .075 * inch

MARGIN = 1 * inch

pcb_w = 6.4 * inch
pcb_h = 9 * inch

# mounting holes
mount_r =  1.5 * mm
corner_holes = array([ ## mount posts
        (        .15 * inch,          .15 * inch, mount_r),
        (        .15 * inch, HEIGHT - .15 * inch, mount_r),
        (WIDTH - .15 * inch,          .15 * inch, mount_r),
        (WIDTH - .15 * inch, HEIGHT - .15 * inch, mount_r)])

# leds
x0 = (WIDTH - pcb_w)/2 + .2 * inch
dx = 0.4 * inch
nx = 16

y0 = 2.05 * inch
dy = 0.7 * inch
ny = 8

led_xs = arange(nx) * dx + x0
led_ys = (arange(ny) * dy + y0)


# In[63]:

# scale size of image
pxpi_x = 100.
pxpi_y = 100.


# In[64]:

english_v3 = '''ITDISPTENTWENTY-
FIVEJHALFQUARTER
PASTOBTWONEIGHTA
THREELEVENSIXTEN
FOURFIVESEVENINE
TWELVELATMINFTHE
MIDNIGHTMORNINGJ
AFTERNOONEVENING
'''

english_v4 = '''
IT IS TWENTYFIVE
TENHALFQUARTER  
PASTO TWONE     
THREELEVENSIXTEN
FOURFIVESEVENINE
TWELVEIGHT  INAT
THEMORNINGNIGHT 
AFTERNOONEVENING
'''


# In[66]:

def build_cells(nrows,ncols,width,height):
    "build the cell location info used in the template"
    cells = []
    cellwidth = width/ncols
    cellheight = height/nrows
    for r in range(nrows):
        for c in range(ncols):
            cells.append({'id'    :'%s%d'%(chr(97+c),r),
                          'title' :'%s %d'%(chr(97+c),r),
                          'left'  : c*cellwidth,
                          'top'   : r*cellheight
                          })
    return cells


# In[75]:

def build_cells(fontpath,fontsize,style,case):
    # init font
    cells = []
    scaledfontsize = pt2pxy(fontsize)
    font = ImageFont.truetype(size=scaledfontsize,filename=fontpath)
    lines = encodeLetters(style,case)

    img = Image.new("RGBA", (pt2pxx(WIDTH), pt2pxy(HEIGHT)))
    draw = Draw(img)

    for i, led_y in enumerate(led_ys):
        for j, led_x in enumerate(led_xs):
            letter = lines[i][j]
            x,y = (pt2pxx(led_x),pt2pxy(led_y))    
            text_width,text_height = font.getsize(letter)
            text_off_x, text_off_y = font.getoffset(letter)   
            # center letter in the grid
            asc,desc = font.getmetrics()

            # adjust to center letter over the led
            x = x - (text_width/2 + text_off_x)
            y = y - (asc+desc)/2
            
            cells.append({'id'    :'%s%d'%(chr(97+i),j),
                          'title' :'%s %d'%(chr(97+i),j),
                          'left'  : x,
                          'top'   : y,
                          'width' : text_width + text_off_x,
                          'height' : asc+desc,
                          })

    del draw
    return cells


if __name__ == '__main__':

    build_cells(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                fontsize=35,
                style=english_v3,
                case=lower)


    img = drawclock(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                    fontsize=35,
                    fgcolor=PALEYELLOW,
                    bgcolor=BLACK,
                    style=english_v3,
                    case=lower,
                    drawLEDs=False)
    img.save('./static/lit.jpg')

    img = drawclock(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                    fontsize=35,
                    fgcolor=GRAY,
                    bgcolor=BLACK,
                    style=english_v3,
                    case=lower,
                    drawLEDs=False)
    img.save('./static/unlit.jpg')





