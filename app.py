from flask import Flask, render_template, abort, send_file, request
from model import Model, APIModel
#from chatbot import chatbot

app = Flask(__name__)

try:
    APIModel().checker()
except:
    print("api model checker exception")

@app.route('/')
def home():
    try:
        data = Model().getAllData()    
        predictions = Model().getPredictions()
        historicalPredictions = Model().getHistoricalPredictions()
        predErrors = Model().getPredictionsErrors()
        return render_template(
            'HomePage.html', 
            data = data, 
            predictions = predictions, 
            historicalPredictions = historicalPredictions,
            predErrors = predErrors
        )
    except:
        abort(500)


@app.route('/awareness')
def awareness():
    try:
        return render_template('AwarenessPage.html')
    except:
        abort(500)

@app.route('/info')
def info():
    try:
        return render_template('InformationPage.html')
    except:
        abort(500)


@app.route('/about')
def about():
    try:
        return render_template('AboutPage.html')
    except:
        abort(500)

@app.route('/worldmap')
def worldmap():
    try:
        return render_template('WorldmapPage.html')
    except:
        abort(500)

@app.route('/chatbot')
def chatbot():
    try:
        return render_template('ChatbotPage.html')
    except:
        abort(500)

@app.route("/get")
def get_bot_response():
    """try:
        userText = request.args.get('msg')
        return str(chatbot.get_response(userText))
    except:
        abort(500)"""



@app.route('/news')
def news():
    try:
        return render_template('NewsPage.html')
    except:
        abort(500)

@app.route('/test')
def test():
    try:
        response = APIModel().makeRequest()
        return response
    except:
        abort(500)

@app.route('/download')
def downloadFile ():
    try:
        name = request.args.get('name')
        if(name=="data"):
            path = "dailyGeneral.csv"
        else:
            path = "predFile.json"
        return send_file(path, as_attachment=True)
    except:
        abort(500)
    #For windows you need to use drive name [ex: F:/Example.pdf]


@app.errorhandler(500)
def internal_error(error):
    return render_template('errorPage.html',
        title= "Erreur interne",
        text= "Une erreur inattendue s'est produite, merci de retourner à la page d'accueil.",
        img= "500.png",
    ), 500
    #return "Une erreur c'est produite, veuillez réessayer",500

@app.errorhandler(404)
def not_found(error):
    return render_template('errorPage.html',
        title= "Erreur 404",
        text= "Cette page n'existe pas, merci de retourner à la page d'accueil.",
        img= "404.png",
    ), 404
    #return "Cette page n'existe pas. Veuillez retourner à la page d'accueil",404

if __name__ == "__main__":
    app.run(debug=True, port=3000)

