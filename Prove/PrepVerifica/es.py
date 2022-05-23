from flask import Flask, render_template, request
import pandas as pd
import geopandas as gpd
app = Flask(__name__)



regioni = gpd.read_file("/workspace/Flask/Prove/PrepVerifica/Regioni.zip")
province = gpd.read_file("/workspace/Flask/Prove/PrepVerifica/Province.zip")
comuni = gpd.read_file("/workspace/Flask/Prove/PrepVerifica/Comuni.zip")

@app.route('/', methods=['GET'])
def home():
    reg = regioni['DEN_REG'].sort_values(ascending=True)
    return render_template('home.html', reg=reg)



@app.route('/reg', methods=['GET'])
def reg():
    regione = request.args['Regioni']
    reg_utente = regioni[regioni['DEN_REG']==regione]
    provReg = province[province.within(reg_utente.geometry.squeeze())]
    prov = province['DEN_PROV'].sort_values(ascending=True)
    return render_template("province.html", prov = provReg["DEN_PROV"])


@app.route('/prov', methods=['GET'])
def prov():
    provincia = request.args['Province']
    prov_utente = province[province['DEN_PROV']==provincia]
    comProv = comuni[comuni.within(prov_utente.geometry.squeeze())]["COMUNE"].reset_index()
    return render_template("result.html", provincia = provincia, tabella = comProv.to_html())









    
    
    

















if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)