from flask import Flask, render_template
from model import Model, APIModel
from datetime import datetime

app = Flask(__name__)

APIModel().checker()

@app.route('/')
def home():
    data = Model().getAllData()    
    predictions = Model().getPredictions()
    historicalPredictions = Model().getHistoricalPredictions()
    return render_template('home.html', data=data, predictions=predictions, historicalPredictions=historicalPredictions)


@app.route('/test')
def test():
    response = APIModel().makeRequest()
    return response

if __name__ == "__main__":
    app.run(debug=True, port=3000)

