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
stazionigeo= gpd.read_file('/workspace/Flask/VerificaA/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv', sep=';')
quartieri= gpd.read_file('/workspace/Flask/AppEs6/ds964_nil_wm-20220322T111617Z-001.zip', sep=';')


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
    nome_quartiere = request.args['quartiere']
    quartiere = quartieri[quartieri.NIL.str.contains(nome_quartiere)]
    stazioni_quartiere = stazionigeo[stazionigeo.within(quartiere.geometry.squeeze())]
    print(quartiere)
    print(stazioni_quartiere)
    print(stazionigeo)

  
    return render_template('elenco1.html', risultato = stazioni_quartiere.to_html())


    







if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)
