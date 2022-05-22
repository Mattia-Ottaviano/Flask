#realizzare un sito web che restituisca la mappa dei quartieri di milano.
#ci deve essere una homepage con un link "quartieri di milano":
#cliccando su questo link si deve visualizzare la mappa dei quartieri di milano 


from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

milano = gpd.read_file('/workspace/Flask/AppEs6/ds964_nil_wm-20220322T111617Z-001.zip')
fontanelle = gpd.read_file('/workspace/Flask/AppEs6/Fontanelle.zip')



@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')









@app.route('/visualizza', methods=['GET'])
def visualizza():
    return render_template('plot.html')
    

@app.route('/plot.png', methods=['GET'])
def plot_png():

    fig, ax = plt.subplots(figsize = (12,8))

    milano.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot', methods=("POST", "GET"))
def mpl():
    return render_template('plot.html',
                           PageTitle = "Matplotlib")







@app.route('/trova', methods=['GET'])
def trova():
    return render_template('str.html')





@app.route('/ricerca', methods = ['GET'])
def ricerca():
    
    quartiere = request.args['Quartiere']
    global risultato
    risultato = milano[milano['NIL']==quartiere.upper()]

    if len(risultato) == 0:
        table = 'quaritere non trovato'
        return render_template('table.html', tabella = table)
    else:
        table = risultato.to_html()
        #caricamento immagine e visualizzazione
        return render_template('plot2.html')


        
@app.route('/plot2.png', methods=['GET'])
def plot2_png():

    fig, ax = plt.subplots(figsize = (12,8))

    risultato.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/scelta', methods=("POST", "GET"))
def plot35():   
    qrt = milano.NIL.to_list()
    qrt.sort()
    return render_template('menu.html', qrt=qrt)





@app.route('/fontmenu', methods=("POST", "GET"))
def fontmenu():   
      return render_template("fontmenu.html", milano= milano["NIL"])



@app.route('/fontanelle', methods=("POST", "GET"))
def font():   
    global imgUtente, fontQuart
    
    quartiereUtente = request.args["Quartiere"]
    imgUtente = milano[milano["NIL"] == quartiereUtente]
    fontQuart = fontanelle[fontanelle.within(imgUtente.geometry.squeeze())]
    print(fontQuart)
    return render_template('fontanelle.html', PageTitle = "Matplotlib", quartiere=quartiereUtente, tabella = fontQuart.to_html())




@app.route("/fontanelle.png", methods=["GET"])
def fontpng():
    fig, ax = plt.subplots(figsize = (12,8))

    imgUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    fontQuart.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)


