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
quartieri= gpd.read_file('/workspace/Flask/VerificaA/ds964_nil_wm-20220322T111617Z-001.zip', sep=';')


@app.route('/', methods=['GET'])
def home():
    return render_template('home1.html')

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta=="es1":
        return redirect(url_for("numero"))
    elif scelta=="es2":
        return redirect(url_for("input"))
    elif scelta=="es3":
        return redirect(url_for("dropdown"))



@app.route('/numero', methods=['GET'])
def numero():
    #numero stazioni per ogni municipio
    global risultato
    risultato=stazioni.groupby("MUNICIPIO")["OPERATORE"].count().reset_index()
    return render_template('elenco.html',risultato=risultato.to_html())

       

@app.route('/grafico', methods=['GET'])
def grafico():
    #costruzione grafico
    fig, ax = plt.subplots(figsize = (6,4))

    x = risultato.MUNICIPIO
    y = risultato.OPERATORE

    ax.bar(x, y, color = "#304C89")
    #visualizzazione grafico

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')



@app.route('/input', methods=['GET'])
def input():

    return render_template('input.html')


@app.route('/ricerca', methods=['GET'])
def ricerca():
    global quartiere, stazioni_quartiere
    nome_quartiere= request.args['quartiere']
    quartiere=quartieri[quartieri.NIL.str.contains(nome_quartiere)]
    stazioni_quartiere= stazionigeo[stazionigeo.within(quartiere.geometry.squeeze())]
    return render_template('elenco1.html',risultato=stazioni_quartiere.to_html())



@app.route('/mappa', methods=['GET'])
def mappa():

    fig, ax = plt.subplots(figsize = (12,8))

    stazioni_quartiere.to_crs(epsg=3857).plot(ax=ax)
    quartiere.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



@app.route('/dropdown', methods=['GET'])
def dropdown():
    nomi_stazioni = stazioni.OPERATORE.to_list()
    nomi_stazioni= list(set(nomi_stazioni))
    nomi_stazioni.sort()
    return render_template('dropdown.html', stazioni = nomi_stazioni)


@app.route('/sceltastazione', methods=['GET'])
def sceltastazione():
    global stazione_utente, quartiere1
    stazione = request.args['stazione']
    stazione_utente = stazionigeo[stazionigeo.OPERATORE==stazione]
    quartiere1 = quartieri[quartieri.contains(stazione_utente.geometry.squeeze())]
    print(quartiere1)

    return render_template('vistastazione.html', quartiere = quartiere1.NIL)


@app.route('/mappaquart', methods=['GET'])
def mappaquart():

    fig, ax = plt.subplots(figsize = (12,8))

    stazione_utente.to_crs(epsg=3857).plot(ax=ax, color='k')
    quartiere1.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



















    







if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
