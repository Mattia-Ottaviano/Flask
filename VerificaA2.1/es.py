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


comuni= gpd.read_file('/workspace/Flask/VerificaA2.1/Comuni.zip')
province = gpd.read_file('/workspace/Flask/VerificaA2.1/Province.zip')
regioni = gpd.read_file('/workspace/Flask/VerificaA2.1/Regioni.zip')


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/input", methods=["GET"])
def input():
    return render_template("input.html")


@app.route("/inserireProv", methods=["GET"])
def inserireProv():
    global prov, info_prov, com_in_prov, area_prov
    prov = request.args['provincia']
    info_prov = province[province['DEN_UTS'].str.contains(prov.title())]
    com_in_prov = comuni[comuni.within(info_prov.geometry.squeeze())]
    area_prov = info_prov.geometry.area/10**6
    return render_template("mappaes1.html", area_prov = area_prov)

@app.route("/mappaes1", methods=["GET"])
def mappaes1():

    fig, ax = plt.subplots(figsize = (12,8))

    info_prov.to_crs(epsg=3857).plot(ax=ax, edgecolor = 'k', facecolor= 'none', linewidth=3)
    com_in_prov.to_crs(epsg=3857).plot(ax=ax, edgecolor="r", facecolor="none")
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

    



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)