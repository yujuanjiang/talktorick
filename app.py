from flask import Flask, request, url_for, redirect, render_template, jsonify
import pandas as pd
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import json
#import keras

app = Flask(__name__)

model = load_model('chat_model')

with open("intents.json") as file:
    data = json.load(file)

# load tokenizer object
with open( 'tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open( 'label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# parameters
max_len = 20


@app.route('/', methods=['POST','GET'])
def home():
    return render_template("home.html")

@app.route('/predict', methods = ['POST', 'GET'])
def predict():

        #inp = request.form.values()[0]
        inp = request.form.get('inp')
        print("inp value is: " + str(inp))
        #inp = 'Hello world!'

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                             truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:
                print("Tag found!!!")
                return render_template('home.html', pred = 'Rick says: ' + i['responses'][0])
                #return render_template('home.html', pred = 'Rick says: '.format(i['responses']))
        
        return render_template('home.html', pred="Response from Rick: {}".format(i['response']))


if __name__ == '__main__':
    app.run(debug=True)
