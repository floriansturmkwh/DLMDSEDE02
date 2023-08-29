import pandas as pd
import data_prep
from pymongo_get_database import get_database
import sys
dbname = get_database()

def read_mongo(collection, filter = None, count= True):
    """ Read from Mongo and Store into DataFrame """
    if filter is not None:
      query = { "symbol": filter}
    else:
      query = {}
    if count == False:
    # put cursor data into dataframe
    # query to the specific DB and Collection
      cursor = dbname[collection].find(query)
      df =  pd.DataFrame(list(cursor))
    else:
    # count the documents in the specific DB and Collection
      records = dbname[collection].count_documents(query) 
      data = {'lines':[records]}
      df = pd.DataFrame(data=data)
    return df

def tts_from_mongo(collection, method):
  df = read_mongo(collection, None, False)
  print(df.shape, file=sys.stderr)
  traindata, testdata = data_prep.split_data(df, method)
  return traindata, testdata