# DLMDSEDE02
This is the project for the course DLMDSEDE02. All code written by Florian Sturm.

How to use the application:
1. Mount a volume called raw_data and transfer any necessary csvs to it
docker volume create raw_data
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Step 2 needs to be repeated on reuse                                                                                   !
! Known Issue: If the csv is too big, the application suffers a catastrophic failure on upload (Out of memory exception).! 
! To prevent this it is suggested to split the csv in mutliple files maxing out at roughly 1.000.000 lines.              !
! Please ensure that all data regarding a stock (symbol) are contained within the same file.                             !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
2. Use docker compose to build the application
docker compose -f docker-compose.mongo.yml up --builddocker volume create raw_data
   The application is executed on localhost and can be accessed using port 8000
2.1. Contact the application to see if it is running
curl localhost:8000/
   This should return a message containing the current time
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Unless a reset of data is wanted or the volume was deleted step 3 does not need repetition for reuse. !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
3. Start the initialize process. Attention: initialize will remove all data from the assigned Volume to guarantee function
curl localhost:8000/initialize/<1>
<1>: filename on data volume incl. file extension (e.g. fh_5yrs_A.csv) 
3.1. If the initial data was split add the additional files using upload. This will add data to the already initialized database.
curl localhost:8000/upload/<1>
<1>: filename on data volume incl. file extension (e.g. fh_5yrs_B.csv)
