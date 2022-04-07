from flask import Flask,render_template, request, Response, redirect, url_for
app = Flask(__name__)

import io
import pandas as pd
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@app.route('/', methods=['GET'])
def home():
    return render_template('home1.html')


@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta=="es1":
        return redirect(url_for("elenco"))
    elif scelta=="es2":
        return redirect(url_for("input"))
    elif scelta=="es3":
        return redirect(url_for("dropdown"))


@app.route('/elenco', methods=['GET'])
def elenco():

    

    return render_template('home1.html')




















if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)