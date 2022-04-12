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

#Dichiarazioni delle dataframe
Mezzi=gpd.read_file('/workspace/Flask/VerificaC/tpl_percorsi_shp (1).zip')
quartieri = gpd.read_file('/workspace/Flask/VerificaC/ds964_nil_wm-20220322T111617Z-001.zip')

#Home
@app.route('/', methods=['GET'])
def home():
    return render_template('home1.html')

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["scelta"]
    if scelta=="es1":
        return redirect(url_for("lunghezzaKm")) #tra gli apici la directory
    elif scelta=="es2":
        return redirect(url_for("sceltaqt"))
    elif scelta=="es3":
        return redirect(url_for("sceltalinea"))

#1. Avere l’elenco delle linee tranviarie e di bus che hanno un percorso la cui lunghezza è compresa tra due valori
#inseriti dall’utente. Ordinare le linee in ordine crescente sul numero della linea.

@app.route('/lunghezzaKm', methods=['GET'])
def lunghezzaKm():
    return render_template('lunghezzaKm.html')

@app.route('/MappaFinale', methods=['GET'])
def MappaFinale():
    global Min,Max,linee_distanza
   
    Min = min(request.args["Kmmin"], request.args["Kmmax"])#ritorna il numero piu piccolo tra i 2 valori
    Max = max(request.args["Kmmin"], request.args["Kmmax"])#ritorna il numero piu grande tra i 2 valori

    linee_distanza = Mezzi[(Mezzi["lung_km"] > Min) & (Mezzi["lung_km"] < Max)].sort_values("linea")
    return render_template("MappaFinale.html", tabella = linee_distanza.to_html())


@app.route("/mappa2.png", methods=["GET"])

def mappa2png():
    

    fig, ax = plt.subplots(figsize = (12,8))


    linee_distanza.to_crs(epsg=3857).plot(ax=ax)
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')




#2.Avere un elenco di tutte le linee (tram e bus) che passano in un certo quartiere. L’utente inserisce il nome del
#quartiere (anche solo una parte del nome) e il sito risponde con l’elenco ordinato in ordine crescente delle linee
#che passano in quel quartiere

@app.route('/sceltaqt', methods=['GET'])
def sceltaqt():
    return render_template('sceltaqt.html')

@app.route('/visualizzamezzi', methods=['GET'])
def visualizzamezzi():
   
    nome_quartiere=request.args["quartiere"]
    quartiere=quartieri[quartieri.NIL.str.contains(nome_quartiere)]
    mezzi_quartiere=Mezzi[Mezzi.intersects(quartiere.geometry.squeeze())]
    mezzi_quartiere=mezzi_quartiere.astype({"linea":int})#solo la colonna divnta un intero 
    
    return render_template('visualizzamezzi.html',risultato=sorted(list(mezzi_quartiere.linea.drop_duplicates()))) #sorted riordina la lista

#3. Avere la mappa della città con il percorso di una linea scelta dall’utente. L’utente sceglie il numero della linea da
#un menù a tendina (le linee devono essere ordinati in ordine crescente), clicca su un bottone e ottiene la mappa
#di Milano con il percorso della linea prescelta

@app.route('/sceltalinea', methods=['GET'])
def sceltalinea():
    global Mezzi
    Mezzi=Mezzi.astype({"linea":int})

    return render_template('sceltalinea.html',Mezzi=sorted(list(Mezzi.linea.drop_duplicates())))


@app.route('/visualizza', methods=['GET'])
def visualizza():
    global Linea_utente
    Linea_utente=request.args["mezzo"]
    return render_template('visualizza.html')

@app.route("/mappa.png", methods=["GET"])
def mappapng():

    fig, ax = plt.subplots(figsize = (12,8))

    quartieri.to_crs(epsg=3857).plot(ax=ax, alpha=0.1)
    mezzi20=Mezzi[Mezzi.linea==Linea_utente]
    mezzi20.to_crs(epsg=3857).plot(ax=ax)
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)