from flask import Flask, render_template
from model import Model

app = Flask(__name__)


@app.route('/')
def home():
    data = Model().getData()    
    predictions = Model().getPredictions()
    return render_template('home.html', data=data, predictions=predictions)


if __name__ == "__main__":
    app.run(debug=True, port=3000)

