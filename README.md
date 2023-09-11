# DLMDSEDE02
This is the project for the course DLMDSEDE02. All code written by Florian Sturm.
## What does this application do:
This application was created to build a data pipeline for the batch processing of stock data. The stock data this app has been built for is based on the Kaggle project: https://www.kaggle.com/datasets/qks1lver/amex-nyse-nasdaq-stock-histories?resource=download
The app consumes a csv and ingests it into a MongoDB from where it can be accessed when a later project needs the data to build a Machine Learning project. The data is validated and preprepared during the ingestion process to provide a consistent quality of data within the database.

## How to use the application:
To load data from a csv into the MongoDB via use of the application the User needs to open a commandline and enter the prompts provided below in the shown order.

1. Mount a volume called raw_data and transfer any necessary csvs to it
   ```
   docker volume create raw_data
   ```
   Data can be transferred by copying it into the local path connected to the volume or through an interface such as Docker Desktop on a Windows machine.
2. Use docker compose to build the application
   > Step 2 needs to be repeated on reuse                                                                                   
   > Known Issue: If the csv is too big, the application can suffer a catastrophic failure on upload (Out of memory exception). 
   > To prevent this it is suggested to split the csv into mutliple files maxing out at roughly 1.000.000 lines.
   > Please ensure that all data regarding a stock (symbol) are contained within the same file.
   ```
   docker compose -f docker-compose.mongo.yml up --build
   ```
   The application is executed on localhost and can be accessed using port 8000
   2.1. Contact the application to see if it is running
      ```
      curl localhost:8000/
      ```
      This should return a message containing the current time
3. Start the initialize process. Attention: initialize will remove all data from the assigned Volume to guarantee function
   ```
   curl localhost:8000/initialize/<1>
   ```
   <1>: filename on data volume incl. file extension (e.g. fh_5yrs_A.csv) 
   3.1. If the initial data was split add the additional files using upload. This will add data to the already initialized database.
   ```
   curl localhost:8000/upload/<1>
   ```
      <1>: filename on data volume incl. file extension (e.g. fh_5yrs_B.csv)
4. The batch process needs to upload the file to the raw_data volume then use the upload procedure to load the data into the mongo db

Further notes:
The functionality of the test train split (tts) and the data ingestion can be verified by using the associated procedures in the app. The training and execution of the model is not part of the project and has only been implemented with placeholders for future use. 

To verify the correct ingestion data can be queried from the MongoDB using:
```
   curl localhost:8000/queryDataCollection
```
if no further input is added this will return a count of the ingested rows.
If a specific stock is to be inspected in more detail its entries can be queried by adding /<Name of Stock>

To verify a correct tts the db can be queried using:
for a split using ScikitLearn: 
```
curl localhost:8000/tts/sklearn
```
for a split using a Random algorithm: 
```
curl localhost:8000/tts/random
```

## Functional manual:
The readme.txt contains this functional manual and can be accessed when the application is running through:
```
   curl localhost:8000/readme
```
The application can be used through localhost at Port 8000. The following commands are available:
- '/': returns current time if application is available 
- '/readme': returns the contents of this functional manual
- '/sources': returns the listing of sources for additional contents as well as the link to the kaggle containing the stock data necessary for use of the app
- '/initialize/<source>': sets up the database from ground up deleting all previous contents to replace prior projects or delete data containing errors. <source> is to be replaced with the file name of the csv which has been uploaded to the filesystem of docker
- '/upload/<source>': adds the contents of a source csv to the already present data in the mongo instance. <source> is to be replaced with the file name of the csv which has been uploaded to the filesystem of docker
- '/queryDataCollection': returns the number of records currently present in the default database
- '/queryDataCollection/<symbol>': <symbol> needs to be replaced with one stock symbol as existent in the database. Returns all entries for this symbol as a dataframe.
- '/tts/<type>': <type> needs to be replaced with either "sklearn" or "random". Splits the available data into training and test data, then shows the count for verification purposes.
- '/trainModel/<model>': dummy function for later implementation. <model> would need to be replaced with the relevant model name
- '/executeModel/<model>': dummy function for later implementation. <model> would need to be replaced with the relevant model name

## Architecture
The application is built with a microservice architecture in mind. The original structure envisioned at the beginning of the process looked like this:

![originalIdea](https://github.com/floriansturmkwh/DLMDSEDE02/assets/111323575/8a45dd55-a731-4c6e-9520-a4c2423b552e)

During the project realization some of those processes have been changed in order and used programming language thus the new architecture looks like  this:

![finalarchitecture](https://github.com/floriansturmkwh/DLMDSEDE02/assets/111323575/684dc156-ec99-4645-ae56-4b82588aaac9)

### Scripts
Each python script serves as a microservice and can be independently extended or adjusted as needed.
#### app.py
This is the main service. It provides the Flask API where a user can access the services provided and described in the functional manual.
#### config.py
The config file contains variables used throughout the other microservices. It can be adjusted to allow use of the application in other contexts and with similar but differently structured raw data. "globals" contain variables that need to be accessed multiple times throughout the application, "procedures" contain associated process keys for the data preparation part of the application.
#### data_prep.py
The data prep service provides the processes for ingesting the raw data and prepreparing it prior to the data being stored in the MongoDB. 
#### modellogic.py
This is a placeholder for the future implementation of the logics to train and use Machine Learning models. 
#### prepare.py
This module contains database related preparation procedures which need to be used to set up the database and connect to it.
#### pymongo_get_database.py
This module is built to contain the database creation and access parameters, which would need to be hidden and improved upon in a productive setting.
#### query_access.py
These are microservices used to access data from the MongoDB
### dockerfiles
These dockerfiles allow the containerized use of the application
#### compose-dev.yaml
This file defines the images needed for the development environment.
#### docker-compose.mongo.yml
This file defines the services and volumes needed to execute the program in a Docker environment.
#### dockerfile
Sets the syntax for the docker execution including making sure to load all requirements for the python scripts to run properly.
#### requirements.txt
Contains all dependencies that need to be loaded prior to executing the python scripts.
