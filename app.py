from flask import Flask, request, jsonify, render_template
import base64, json
from pprint import pprint
import numpy as np
import flask
import evaluation

# declare constants
HOST = '0.0.0.0'
PORT = 8888

# initialize flask application
app = Flask(__name__)



@app.route('/')
def home():

    return render_template("home.html")


@app.route('/predict', methods=['GET','POST'])
def predict():
    fname = [x for x in request.form.values()]
    label, predicted, time = evaluation._predict(fname[0])
    return flask.render_template('home.html', label_text=label,
                                 predict_text=predicted, time_predict=time)

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)
