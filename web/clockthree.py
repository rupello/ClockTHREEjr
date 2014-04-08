
from flask import Flask, render_template


app = Flask(__name__)

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


@app.route('/')
@app.route('/index')
def index():
    return render_template('clock.html',cells=build_cells(nrows=9,ncols=10,width=1080,height=720))


#!flask/bin/python
if __name__ == '__main__':
    app.run(debug = True)