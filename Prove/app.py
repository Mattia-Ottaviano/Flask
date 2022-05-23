from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    testo = "Welcome"
    return render_template("index.html", testo = testo)

@app.route('/it', methods=['GET'])
def Ciao_Mondo():
    testo = "Benvenuto"
    return render_template("index.html", testo = testo)

@app.route('/fr', methods=['GET'])
def Bonjour():
    testo = "Bonjour"
    return render_template("index.html", testo = testo)


@app.route('/data', methods=['GET'])
def data():
    testo = "Bonjour"
    return render_template("index.html", testo = testo)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)

