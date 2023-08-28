from dateutil import parser
from pymongo_get_database import get_database

import data_prep

def initialize(URL, collection):
  #reset db then upload csv for basic set
  reset_mongo(collection)
  insert_mongo(URL, collection)
  
def upload(URL, collection):
  #add set to db
  insert_mongo(URL, collection)

def insert_mongo(URL, collection):
  #provide db connection, then insert contents of csv
  dbname = get_database()
  collection_name = dbname[collection]

  input_dict = data_prep.data_ingest(URL)
  if len(input_dict) > 0:
    collection_name.insert_many(input_dict)
  return str(len(input_dict))

def reset_mongo(collection):
  #delete collection for new project
  dbname = get_database()
  collection_name = dbname[collection]
  collection_name.drop()
