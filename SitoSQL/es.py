from flask import Flask,render_template, request
app = Flask(__name__)

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)