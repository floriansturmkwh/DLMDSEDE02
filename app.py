import json
import prepare
import query_access
import config
import sys
import os
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
    return 'Application available. Current time: ' + str(datetime.now())

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
    

@app.route('/trainModel')
def train():
    return "Todo Train"

@app.route('/executeModel')
def execute():
    return "Todo Execute"

if __name__ == "__main__":
    app.run(host ='0.0.0.0')