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
print(milano)

@app.route('/', methods=['GET'])
def search():
    return render_template('search.html')
    

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




@app.route('/trova', methods = ['GET'])
def trova():
    
    quartiere = request.args['quartiere']
    
    risultato = milano[milano['NIL']==quartiere.upper()]
    if len(risultato) == 0:
        table = 'quaritere non trovato'
        return render_template('table.html', tabella = table)
    else:
        table = risultato.to_html()
        #caricamento immagine e visualizzazione
        
    





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)


