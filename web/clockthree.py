
from flask import Flask, render_template, jsonify
import Simulate
import clockwords
from clockface import build_cells, english_v3
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


@app.route('/map')
def map():
    data = Simulate.readwtf('langs/English_v3.wtf')
    return clockwords.data2json(data)


#!flask/bin/python
if __name__ == '__main__':
    app.run(debug = True)