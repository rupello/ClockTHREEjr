import os
from flask import Flask, render_template, abort
import Simulate
import clockwords
from clockface import build_cells
from string import lower,upper


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    data = Simulate.readwtf('langs/English_v3.wtf')
    return render_template('clock.html',
                           cells=build_cells(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                                                          fontsize=35,
                                                          style=data['letters'],
                                                          case=lower))

# TODO add dynamic clock face generation
# TODO add lang selection eg /clockthreejr/English_v3/

def findwtf(style):
    for dirpath,dirnames,fnames in os.walk('./langs'):
        for f in fnames:
            name,ext = os.path.splitext(f)
            if ext.lower()=='.wtf':
                if style.lower()==name.lower():
                    return os.path.join(dirpath,f)


@app.route('/clock3jr/<style>/map')
def map(style):
    wtfpath = findwtf(style)
    if wtfpath is not None:
        data = Simulate.readwtf(wtfpath)
        return clockwords.data2json(data)
    else:
        abort(404)


@app.route('/clock3jr/<style>/')
def clock3jr(style):
    wtfpath = findwtf(style)
    if wtfpath is not None:
        data = Simulate.readwtf(wtfpath)
        return render_template('clock.html',
                               cells=build_cells(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                                                 fontsize=35,
                                                 style=data['letters'],
                                                 case=lower))
    else:
        abort(404)

#!flask/bin/python
if __name__ == '__main__':
    app.run(debug = True)