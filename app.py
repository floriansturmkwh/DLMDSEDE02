import json
import prepare
import query_access
import config
import sys
import os
import modellogic #not functional
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)
data_collection = config.globals["data_collection"]
models_collection = config.globals["model_collection"]

@app.route('/')
def response_test():
    return 'Application available. Current time: ' + str(datetime.now()) + ' Available functions can be found in the readme. curl localhost:8000/readme'

@app.route('/readme')
def readme():
    txt = Path('readme.txt').read_text()
    return txt

@app.route('/sources')
def sources():
    txt = Path('sources.txt').read_text()
    return txt

@app.route('/initialize/<source>')
def initialize(source):
    URL =  os.path.relpath('../raw_data/' + source)
    prepare.initialize(URL, data_collection)
    return "success"
    #df = query_access.read_mongo(data_collection, None)
    #return "Shape = {}".format(df.shape)

@app.route('/upload/<source>')
def upload(source):
    URL = "../raw_data/" + source
    prepare.upload(URL, data_collection)
    return "success"
    #df = query_access.read_mongo(data_collection, None)
    #return "Shape = {}".format(df.shape)

@app.route('/queryDataCollection', defaults={'symbol': None})
@app.route('/queryDataCollection/<symbol>')
def query(symbol):
    #query data collection
    if symbol is not None:
      df = query_access.read_mongo(data_collection, symbol, False)
      return "Shape = {}".format(df.shape)
    else:
      df = query_access.read_mongo(data_collection)
      return df.to_string()

@app.route('/tts/<type>')
def tts(type):
    # test for verifying correct tts function as real training is not implemented
    traindata, testdata = query_access.tts_from_mongo(data_collection, type)
    return("Train Shape = {}".format(traindata.shape) + "/ Test Shape = {}".format(testdata.shape))

@app.route('/trainModel/<model>')
def train(model):
    traindata, testdata = query_access.tts_from_mongo(data_collection, type)
    model = modellogic.train(model, traindata, testdata)
    return "Training the model is not implemented as part of the project"

@app.route('/executeModel/<model>')
def execute(model):
    data = modellogic.execute(model)
    return "Executing the model is not implemented as part of the project"

if __name__ == "__main__":
    app.run(host ='0.0.0.0')