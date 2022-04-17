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
        return render_template('elencoProv.html', province = province['DEN_UTS'].sort_values(ascending=True))
    elif scelta=="es3":
        return render_template('elencoReg.html', regioni = regioni['DEN_REG'].sort_values(ascending=True))

#ES1
@app.route('/input', methods=['GET'])
def input():
    com_user = request.args['com']
    global info_com,com_limitrofi, area_com
    info_com = comuni[comuni.COMUNE.str.contains(com_user)]
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

#ES2
@app.route("/elencoProv", methods=["GET"])
def elencoProv():
    global prov, info_prov, com_in_prov
    prov = request.args['provincia']
    info_prov = province[province['DEN_UTS'].str.contains(prov.title())]
    com_in_prov = comuni[comuni.within(info_prov.geometry.squeeze())]
    return render_template("elencoCom.html", com_in_prov = com_in_prov['COMUNE'].sort_values(ascending=True))


@app.route("/elencoCom", methods=["GET"])
def elencoCom():
    
    return render_template('mappaCom.html', com = com_limitrofi.to_html(), area = area_com)

#ES3
@app.route("/elencoReg", methods=["GET"])
def elencoReg():
    reg = request.args['regione']
    info_reg = regioni[regioni['DEN_REG'].str.contains(reg.title())]
    prov_in_reg = province[province.within(info_reg.geometry.squeeze())]
    return render_template("elencoProv.html", province = prov_in_reg['DEN_PROV'].sort_values(ascending=True))






if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)