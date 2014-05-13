
from flask import Flask, render_template, jsonify
import Simulate
import clockwords
from clockface import build_cells, english_v3
from string import lower,upper


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('clock.html',
                           cells=build_cells(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                                                          fontsize=35,
                                                          style=english_v3,
                                                          case=lower))

#var mapdata=null;
#$.getJSON('map',function(data) {mapdata=data;});
#$('.lit').hide()
#$(mapdata.words['it']).show()

@app.route('/map')
def map():
    data = Simulate.readwtf('langs/English_v2.wtf')
    return clockwords.data2json(data)


#!flask/bin/python
if __name__ == '__main__':
    app.run(debug = True)