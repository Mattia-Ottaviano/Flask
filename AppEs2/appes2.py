#realizzare un sito web che permetta la registrazione degli utenti
# l'utente inserisce il nome, uno username, una password
# la conferma della password e il sesso. FATTO

# se le informazioni sono corrette il sito salva le informazioni in una struttura dati opportuna(lista dizionari).FATTO
#prevedere la possibilità di fare il log-in inserendo username e password. FATTO
# se sono corrette, fornire un messaggio di benvenuto diverso a seconda del sesso. FATTO

from flask import Flask,render_template, request
app = Flask(__name__)
lst= []
 

@app.route('/', methods=['GET'])       #home page
def home():
    return render_template('registrazione.html') # mi viene restituito "registrazione.html"


@app.route('/dates', methods=['GET'])  
def dates():
    Name = request.args['Name']
    Pass = request.args['Pass']
    Username = request.args['User']
    Confirm = request.args['Conf']
    Sex = request.args['Sex']

    
    if Pass==Confirm:
       lst.append({'name':Name,'username':Username,'password':Pass,'sex':Sex})
       print(lst)
       return render_template('login.html')
    else:
        return render_template('ConfPass.html')



@app.route('/login', methods=['GET'])
def login():
    username_log = request.args['User']
    password_log = request.args['Pass']
    for utente in lst:
        if utente['username'] == username_log and utente['password'] == password_log:
            if utente['sex'] == 'M':
                return render_template('welcome.html', nome=utente['name'])
            else:
                return render_template('welcomeW.html', nome=utente['name'])

    return render_template('error.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)