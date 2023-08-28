from pandas import Index

globals = { "csv_seperator": ',' # Seperator in a csv-file
          , "csv_encoding": 'UTF-8' # Encoding of the csv
          , "expectedHeaders": ['date','volume','open','high','low','close','adjclose','symbol']
          , "groupField": 'symbol'
          , "data_collection": 'DLMDSEDE02data'
          , "model_collection": 'DLMDSEDE02models'
          }
procedures = {"date": "removeRow",
              "volume": "removeRow",
              "open": "removeRow",
              "high": "removeRow",
              "low": "removeRow",
              "close": "removeRow",
              "adjclose": "removeRow",
              "symbol": "removeRow"
}