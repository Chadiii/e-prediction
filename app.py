from flask import Flask, render_template, abort
from model import Model, APIModel

app = Flask(__name__)

APIModel().checker()

@app.route('/')
def home():
    try:
        data = Model().getAllData()    
        predictions = Model().getPredictions()
        historicalPredictions = Model().getHistoricalPredictions()
        predErrors = Model().getPredictionsErrors()
        return render_template(
            'home.html', 
            data = data, 
            predictions = predictions, 
            historicalPredictions = historicalPredictions,
            predErrors = predErrors
        )
    except:
        abort(500)


@app.route('/test')
def test():
    try:
        response = APIModel().makeRequest()
        return response
    except:
        abort(500)


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

