next-price
----------

## How to run

1. Assuming you have pip installed, install other dependencies.
``` bash
$ sudo pip install flask pandas pandas_datareader scikit-learn numpy pickle
```

2. Run the following to start the server.
``` bash
$ python server.py
```

3. Open your browser and go to `http://127.0.0.1:5000/`.

## Files
- server.py

Main file which hosts the HTTP flask server. Contains a list of endpoints
and the function to run when it is called.

- db.py

Contains all the database queries that are made during the process.
Queries are made for plotting the graph, making predictions, to display
statistics etc.

- FuturePredict.py

Given a Company and the type of data to predict, it pulls an initial data and
invokes the functions to predict the future stock values

- predict.py

Given a Company , type of data and time period invokes functions to pull the
data and train and save models for various regression algorithms

- helperfunc.py

Contains all the functions needed by predict.py and FuturePredict.py to perform
training and prediction of stock market values

- data/historical.py

Contains API call that are made for historical data collection.
Then it inserts the data to database.

- data/realtime.py

Contains code that runs constantly in the background that collects realtime 
data from the Yahoo! Finance API. Then it inserts the data into the realtime
table in the sqlite database.

## Contributors
Sanjay, Anivesh, Soundar
