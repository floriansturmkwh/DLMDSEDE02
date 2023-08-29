# DLMDSEDE02
This is the project for the course DLMDSEDE02. All code written by Florian Sturm.
See readme.txt for functional manual. Can also be found when the application is running through curl localhost:8000/readme
How to use the application:
1. Mount a volume called raw_data and transfer any necessary csvs to it
docker volume create raw_data
!Step 2 needs to be repeated on reuse                                                                                   
!Known Issue: If the csv is too big, the application can suffer a catastrophic failure on upload (Out of memory exception). 
!To prevent this it is suggested to split the csv into mutliple files maxing out at roughly 1.000.000 lines.
!Please ensure that all data regarding a stock (symbol) are contained within the same file.
2. Use docker compose to build the application
docker compose -f docker-compose.mongo.yml up --build
   The application is executed on localhost and can be accessed using port 8000
2.1. Contact the application to see if it is running
curl localhost:8000/
   This should return a message containing the current time
3. Start the initialize process. Attention: initialize will remove all data from the assigned Volume to guarantee function
curl localhost:8000/initialize/<1>
<1>: filename on data volume incl. file extension (e.g. fh_5yrs_A.csv) 
3.1. If the initial data was split add the additional files using upload. This will add data to the already initialized database.
curl localhost:8000/upload/<1>
<1>: filename on data volume incl. file extension (e.g. fh_5yrs_B.csv)
4. The batch process needs to upload the file then use the upload procedure to load the data into the mongo db

Further notes:
The functionality of the test train split (tts) and the data ingestion can be verified by using the associated procedures in the app. The training and execution of the model is not part of the project and has only been implemented with placeholders for future use. 

To verify the correct ingestion data can be queried from the MongoDB using:
curl localhost:8000/queryDataCollection
if no further input is added this will return a count of the ingested rows.
If a specific stock is to be inspected in more detail its entries can be queried by adding /<Name of Stock>

To verify a correct tts the db can be queried using:
for a split using ScikitLearn: curl localhost:8000/tts/sklearn
for a split using a Random algorithm: curl localhost:8000/tts/random

