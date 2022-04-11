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

#ESERCIZIO 1

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


#ESERCIZIO 2

@app.route('/trova', methods=['GET'])
def trova():
    return render_template('inputquart.html')


@app.route('/ricerca', methods=['GET'])
def ricerca():
    quartiere_input = request.args['quartiere']
    print(quartiere_input)
    global info_quartiere, stazioni_quartiere
    info_quartiere = quartieri[quartieri.NIL.str.contains(quartiere_input.upper())]
    print(info_quartiere)
    stazioni_quartiere = stazionigeo[stazionigeo.within(info_quartiere.geometry.squeeze())]

    if len(info_quartiere) == 0:
        risultato = 'quaritere non trovato'
        return render_template('erroreinputes2.html', risultato = risultato)
    else:
        
        return render_template('mappa.html')


@app.route('/mappa', methods=['GET'])
def mappa():

    fig, ax = plt.subplots(figsize = (12,8))

    stazioni_quartiere.to_crs(epsg=3857).plot(ax=ax, color='k')
    info_quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)

    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


#ESERCIZIO 3


@app.route('/grafico', methods=['GET'])
def grafico():
    #numero stazioni per ogni municipio
    global risultato
    risultato=stazioni.groupby("MUNICIPIO")["UBICAZIONE"].count().reset_index()
    return render_template('grafico.html',risultato=risultato.to_html())



@app.route('/outputgrafico', methods=['GET'])
def outputgrafico():
    
    fig, ax = plt.subplots(figsize = (6,4))

    x = risultato.MUNICIPIO
    y = risultato.UBICAZIONE
    ax.bar(x, y, color = "#304C89")
    
    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')

    
    




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)