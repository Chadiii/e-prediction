from flask import Flask, render_template, abort, request
from model import Model, APIModel
from chatbot import chatbot as cb

app = Flask(__name__)

try:
    APIModel().checker()
except:
    print("api model checker exception")

try:
    APIModel().bgScheduler()
    APIModel().sched.start()
except:
    print("api model bgScheduler exception")

@app.route('/')
def home():
    try:
        data = Model().getAllData()    
        predictions = Model().getPredictions()
        historicalPredictions = Model().getHistoricalPredictions()
        predErrors = Model().getPredictionsErrors(historicalPredictions)
        accuracy = Model().getAccuracy(historicalPredictions)
        worldTopCounries = APIModel().getWorldTopCounries()
        if(len(data)>0):
            resume = data[len(data)-1]
        if(len(predictions)>=2):
            resume["prediction1"] = predictions[0]
            resume["prediction2"] = predictions[1]
        return render_template(
            'HomePage.html', 
            data = data, 
            predictions = predictions, 
            historicalPredictions = historicalPredictions,
            predErrors = predErrors,
            resume = resume,
            accuracy = accuracy,
            worldTopCounries = worldTopCounries,
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

@app.route("/get_bot_response")
def get_bot_response():
    userText = request.args.get('msg')
    return str(cb.get_response(userText))
    """try:
    except:
        abort(500)"""



@app.route('/news')
def news():
    try:
        return render_template('NewsPage.html')
    except:
        abort(500)

@app.route('/update')
def update():
    try:
        response = APIModel().makeRequest()
        return response
    except:
        abort(500)

@app.route('/check')
def downloadFile ():
    try:
        name = request.args.get('name')
        if name is None:
            return "<ul> <li><a href='/check?name=data'>Data</a></li> <li><a href='/check?name=pred'>Predictions</a></li> </ul>"
        elif(name=="data"):
            return Model().showData()
        else:
            return Model().showPredictions()
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

