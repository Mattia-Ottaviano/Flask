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


comuni= gpd.read_file('/workspace/Flask/VerificaA2/Comuni.zip')
province = gpd.read_file('/workspace/Flask/VerificaA2/Province.zip')
regioni = gpd.read_file('/workspace/Flask/VerificaA2/Regioni.zip')
print(comuni)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["radio"]
    if scelta=="es1":
        return render_template('input.html')
    elif scelta=="es2":
        return redirect(url_for("input"))
    elif scelta=="es3":
        return redirect(url_for("dropdown"))

  
@app.route('/input', methods=['GET'])
def input():
    com_user = request.args['com']
    global info_com,com_limitrofi
    info_com = comuni[comuni.COMUNE.str.contains(com_user.title())]
    area_com = info_com.geometry.area/10**6
    com_limitrofi = comuni[comuni.touches(info_com.geometry.squeeze())].sort_values(by='COMUNE', ascending=True)
    return render_template('mappaCom.html', com = com_limitrofi.to_html(), area = area_com)


@app.route("/mappaCom", methods=["GET"])
def mappaCom():

    fig, ax = plt.subplots(figsize = (12,8))

    info_com.to_crs(epsg=3857).plot(ax=ax, edgecolor = 'k', facecolor= 'none')
    com_limitrofi.to_crs(epsg=3857).plot(ax=ax, edgecolor="k", facecolor="r", alpha=0.2)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)