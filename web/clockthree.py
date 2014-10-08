import os
from string import lower,upper
import StringIO

import flask
from flask import Flask, render_template, abort, Response, request, current_app
import ttfquery
from flask_bootstrap import Bootstrap

import Simulate
import clockwords
import clockface
import wtfhelpers

def create_app():
    "create a configures app instance"
    app = Flask(__name__)
    Bootstrap(app)

    fontreg = ttfquery.ttffiles.Registry()
    fontreg.scan('./fonts/')
    app.config['wtfs'] = wtfhelpers.loadwtfsandfonts('./langs/',fontreg)
    app.config['fontregistry'] = fontreg
    return app

# the app
app = create_app()

def findwtf(style):
    "find the path to the .wrf file"
    for dirpath,dirnames,fnames in os.walk('./langs'):
        for f in fnames:
            name,ext = os.path.splitext(f)
            if ext.lower()=='.wtf':
                if style.lower()==name.lower():
                    return os.path.join(dirpath,f)


def default_font(style):
    return current_app.config['wtfs'][style.lower()]['fonts'][0]


def findfontpath(style,fontname):
    for fontpath in current_app.config['wtfs'][style.lower()]['fonts']:
        if font_name_from_path(fontpath)==fontname:
            return fontpath
    return default_font(style)


@app.template_filter('fontname')
def font_name_from_path(path):
    return os.path.basename(path).lower()


@app.route('/')
@app.route('/index')
def index():
    return flask.redirect("/clock3jr/styles/", code=302)


@app.route('/clock3jr/<style>/clockface')
def clockfaceimg(style):
    wtfpath = findwtf(style)
    if wtfpath is not None:
        data = Simulate.readwtf(wtfpath)
        fgcolor = request.args.get('fg', '#303030')
        fontname = request.args.get('font')
        #img = clockface.drawclock(fontpath=r"./fonts/JosefinSans-Regular.ttf",
        img = clockface.drawclock(fontpath=findfontpath(style,fontname),
                                    fontsize=30,
                                    fgcolor=fgcolor,
                                    bgcolor=clockface.BLACK,
                                    style=data['letters'],
                                    case=lower,
                                    drawLEDs=False)
        io = StringIO.StringIO()
        img.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')
    else:
        abort(404)


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
        fontname = request.args.get('font')
        data = Simulate.readwtf(wtfpath)
        return render_template('clock.html',
                               cells=clockface.build_cells(fontpath=findfontpath(style,fontname),
                                                            fontsize=40,
                                                            style=data['letters'],
                                                            case=lower),
                               style=style,
                               fontname=fontname)
    else:
        abort(404)

@app.route('/clock3jr/styles/')
def styles():
    wtfs = current_app.config['wtfs']
    return render_template('styles.html',styles=['foo','bar'],wtfs=wtfs)


#!flask/bin/python
if __name__ == '__main__':
    app.run(debug = True)