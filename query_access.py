import pandas as pd
from pymongo_get_database import get_database
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