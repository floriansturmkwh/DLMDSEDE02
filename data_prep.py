import pandas as pd
import numpy
import sys
import config
from sklearn.model_selection import train_test_split

def data_ingest(URL):
    #read csv from path
    input = pd.read_csv(filepath_or_buffer=URL,
                        sep=config.globals["csv_seperator"],
                        encoding=config.globals["csv_encoding"])
    # validate data to fit with expected
    if chk_headers(input):
      #use prepreparation logic
      prepared = prepare_data(input)
      #turns dataframe into list of dictionaries
      input_dict = prepared.to_dict('records') 
    else:
      input_dict = []
    return(input_dict)

def chk_headers(data):
    #check against config
    headers = data.keys()
    if data.columns.to_numpy().tolist() == config.globals["expectedHeaders"]:
        return True
    else:
        return False

def add_mean(data):
  # adding the mean of the close grouped for each stock
  mean_close = data.groupby('symbol')['close'].mean()
  mean_data = mean_close.to_frame()
  data2 = mean_data.rename(columns={'close':'mean_close'})
  added = pd.merge(data, data2, how='inner', on=['symbol'])
  return added

def add_normalized(data):
    # "normalizes" all columns based on the mean close of each stock
    data['n_open']     = data['open']    /data['mean_close']
    data['n_high']     = data['high']    /data['mean_close']
    data['n_low']      = data['low']     /data['mean_close']
    data['n_close']    = data['close']   /data['mean_close']
    data['n_adjclose'] = data['adjclose']/data['mean_close']
    return data
    
def prepare_data(data):
   #process rows with empty fields
   fieldnames = data.columns.to_numpy().tolist()
   #debug print(fieldnames, file=sys.stderr) 
   for fieldname in fieldnames:
     # check for empty cells and treat them based on definition in config
     #debug print(fieldname, file=sys.stderr)
     procedure = config.procedures[fieldname]
     # for use case it is not useful to use average, ffill or bfill 
     # those further methods can be used if column composition changes
     if procedure == 'removeRow':
       data.dropna(subset=[fieldname],axis=0,inplace=True)
     elif procedure == 'last':
       data[fieldname].fillna(method = 'ffill')
     elif procedure == 'next':
       data[fieldname].fillna(method = 'bfill')
   # add a column with the mean value at closing for each stock (Symbol)
   data = add_mean(data)
   # create new relative columns based on values divided by the mean
   data = add_normalized(data)
   return data

def split_data(df, method):
  if method == "sklearn":
    train, test = train_test_split(df, test_size=config.globals["testsplit"])
    return train, test
  elif method == 'random':
    msk = numpy.random.rand(len(df)) < (1-config.globals["testsplit"])
    train = df[msk]
    test=df[~msk]
    return train, test
  else:
    return pd.DataFrame(),pd.DataFrame()