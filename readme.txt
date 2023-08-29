The application can be used through localhost at Port 8000. The following commands are available:
'/': returns current time if application is available 
'/readme' returns the contents of this file
'/sources' returns the listing of sources for additional contents as well as the link to the kaggle containing the stock data necessary for use of the app
'/initialize/<source>' sets up the database from ground up deleting all previous contents to replace prior projects or delete data containing errors. <source> is to be replaced with the file name of the csv which has been uploaded to the filesystem of docker
'/upload/<source>' adds the contents of a source csv to the already present data in the mongo instance. <source> is to be replaced with the file name of the csv which has been uploaded to the filesystem of docker
'/queryDataCollection' returns the number of records currently present in the default database
'/queryDataCollection/<symbol>' <symbol> needs to be replaced with one stock symbol as existent in the database. Returns all entries for this symbol as a dataframe.
'/tts/<type>' <type> needs to be replaced with either "sklearn" or "random". Splits the available data into training and test data, then shows the count for verification purposes.
'/trainModel/<model>' dummy function for later implementation. <model> would need to be replaced with the relevant model name
'/executeModel/<model>' dummy function for later implementation. <model> would need to be replaced with the relevant model name