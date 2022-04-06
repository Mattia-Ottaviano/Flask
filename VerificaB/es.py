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


stazioni=pd.read_csv('/workspace/Flask/VerificaA/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv', sep=';')
stazionigeo= gpd.read_file('/workspace/Flask/VerificaA/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson', sep=';')
quartieri= gpd.read_file('/workspace/Flask/AppEs6/ds964_nil_wm-20220322T111617Z-001.zip', sep=';')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/scelta', methods=['GET'])
def scelta():
    return render_template('radquart.html', quartieri = quartieri['NIL'].sort_values(ascending=True))


@app.route('/radquart', methods=['GET'])
def radquart():
    quartiere_scelto = request.args['quartiere']
    print(quartiere_scelto)
    info_quartiere = quartieri[quartieri.NIL.str.contains(quartiere_scelto)]
    print(info_quartiere)
    staz_in_quart = stazionigeo[stazionigeo.within(info_quartiere.geometry.squeeze())]
    
    return render_template('elencostazioni.html',risultato=staz_in_quart.to_html())

















if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)