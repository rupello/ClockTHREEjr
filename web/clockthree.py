
from flask import Flask, render_template
from clockface import build_cells, english_v4
from string import lower,upper

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('clock.html',
                           cells=build_cells(fontpath=r"./fonts/JosefinSans-Regular.ttf",
                                                          fontsize=35,
                                                          style=english_v4,
                                                          case=lower))


#!flask/bin/python
if __name__ == '__main__':
    app.run(debug = True)