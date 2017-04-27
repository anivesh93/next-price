from __future__ import print_function
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVC, SVR
import os
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from datetime import  timedelta, date
import pandas_datareader.data as web
import sqlite3

def getStock(symbol, start, end):

    df = web.DataReader(symbol, 'yahoo', start, end)

    print(df.head())

    df = df[['Close']]
    df.columns.values[-1] = 'Close'
    df.columns = df.columns + '_' + symbol
    df['Return_%s' %symbol] = df['Close_%s' %symbol].pct_change()

    print(df.head())

    return df

def getRealTime(symbol):

    con = sqlite3.connect("data/stocks.db")
    query = 'SELECT * FROM realtime WHERE symbol="{0}";';
    df = pd.read_sql_query(query.format(symbol), con)

    dfa = df[['price']]
    dfb = df[['date','time']]
    dfa.index = pd.MultiIndex.from_arrays(dfb.values.T)

    df = dfa
    df.columns.values[-1] = 'Close'
    df.columns = df.columns + '_' + symbol
    df['Return_%s' %symbol] = df['Close_%s' %symbol].pct_change()

    con.close()
    return df

def getRealTimePredict(symbol):

    con = sqlite3.connect("data/stocks.db")
    query = 'SELECT * FROM realtime WHERE SYMBOL = "{0}" ORDER BY DATE,TIME DESC LIMIT 15'
    df = pd.read_sql_query(query.format(symbol), con)

    dfa = df[['price']]
    dfb = df[['date','time']]
    dfa.index = pd.MultiIndex.from_arrays(dfb.values.T)

    df = dfa
    df.columns.values[-1] = 'Close'
    df.columns = df.columns + '_' + symbol
    df['Return_%s' %symbol] = df['Close_%s' %symbol].pct_change()
    date = dfb.get_value(14,'date')+" "+dfb.get_value(14,'time')

    con.close()
    return df,date

def getReturns(df,symbol):


    df.columns.values[-1] = 'Close'
    df.columns = df.columns + '_' + symbol
    df['Return_%s' %symbol] = df['Close_%s' %symbol].pct_change()

    return df

def addFeatures(dataframe, adjclose, returns, n):

    return_n = adjclose[9:] + "Time" + str(n)
    dataframe[return_n] = dataframe[adjclose].pct_change(n)
    
    roll_n = returns[7:] + "RolMean" + str(n)
    dataframe[roll_n] = pd.rolling_mean(dataframe[returns], n)

    exp_ma = returns[7:] + "ExponentMovingAvg" + str(n)
    dataframe[exp_ma] = pd.ewma(dataframe[returns], halflife=30)

# REGRESSION
def performRegression(traindata, testdata, split, symbol, output_dir, data_type):

    #features = dataset.columns[1:]
    index = int(np.floor(traindata.shape[0]*split))
    train , test = traindata[:index], traindata[index:]

    trainl, testl = testdata[:index], testdata[index:]
    print('Size of train set: ', train.shape, trainl.shape)
    print('Size of test set: ', test.shape, testl.shape)

    out_params = (symbol, output_dir)

    #output = dataset.columns[0]

    predicted_values = []

    classifiers = [
        RandomForestRegressor(n_estimators=10, n_jobs=-1),
        SVR(C=100000, kernel='rbf', epsilon=0.1, gamma=1, degree=2),
        BaggingRegressor(),
        AdaBoostRegressor(),
        KNeighborsRegressor(),
        GradientBoostingRegressor(),
        MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    ]


    for classifier in classifiers:

        predicted_values.append(benchmark_model(classifier, train, test, trainl, testl, out_params, symbol, data_type))


    print('-'*80)

    mean_squared_errors = []

    r2_scores = []


    for pred in predicted_values:
        mean_squared_errors.append(mean_squared_error(testl, pred))
        r2_scores.append(r2_score(testl, pred))


    print(mean_squared_errors, r2_scores)

    return mean_squared_errors, r2_scores


def benchmark_model(model, train, test, trainl, testl, output_params, symbol, data_type, *args, **kwargs):

    print('-'*80)
    model_name = model.__str__().split('(')[0].replace('Regressor', ' Regressor')
    print(model_name)

    symbol, output_dir = output_params

    if(model_name == "MLPClassifier"):
        trainlabels = np.asarray(trainl, dtype="|S6")
    else:
        trainlabels = trainl

    model.fit(train, trainlabels, *args, **kwargs)

    from sklearn.externals import joblib

    filename = symbol +"_"+ model_name +"_"+ data_type +".pkl"
    joblib.dump(model,"data/models/"+filename)

    for i in range(1,test.shape[0]+1):
        testd = test[i-1:i]
        if(i == 1):
            predicted_value = model.predict(testd)
            if(model_name == "MLPClassifier"):
                predicted_value = predicted_value.astype(np.float)
            pred = np.array(predicted_value)
        else:
            predicted_value = model.predict(temptest)
            if(model_name == "MLPClassifier"):
                predicted_value = predicted_value.astype(np.float)
            pred = np.append(pred, predicted_value)



        d = {'$close':[testd[0,20],predicted_value]}
        new_df = pd.DataFrame(d)
        new_df.columns = ['close']
        new_df = getReturns(new_df,symbol)
        columns = new_df.columns
        close = columns[-2]
        returns = columns[-1]
        addFeatures(new_df,close, returns, 1)


        temptest = np.array(testd[0,5:25])
        for j in range(0,5):
            temptest = np.append(temptest,new_df.iloc[1][j])

        temptest = temptest.reshape(1,25)


    plt.plot(testl, color='g', ls='-', label='Actual Value')
    plt.plot(pred, color='b', ls='--', label='predicted_value Value')

    plt.xlabel('Number of Set')
    plt.ylabel('Output Value')

    plt.title(model_name)
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, str(symbol) + '_' + model_name + '.png'), dpi=100)

    plt.clf()

    return pred


def futurepredict(Testdata,Testlabel, symbol, startdate, model_name,data_type):

    predict = []
    if(data_type == "hist"):
        date = startdate + timedelta(days=2)
    else:
        date = startdate + timedelta(minutes=2)

    filename = symbol +"_"+ model_name +"_"+ data_type +".pkl"
    model = joblib.load("data/models/"+filename)

    if(model_name == "MLPClassifier"):
        Testlabel = np.asarray(Testlabel, dtype="|S6")
    else:
        Testlabel = Testlabel


    for i in range(1,Testdata.shape[0]+22):

        testd = Testdata[i-1:i]
        if(i == 1):
            predicted_value = model.predict(testd)
            if(model_name == "MLPClassifier"):
                predicted_value = predicted_value.astype(np.float)
            pred = np.array(predicted_value)
        else:
            predicted_value = model.predict(temptest)
            if(model_name == "MLPClassifier"):
                predicted_value = predicted_value.astype(np.float)
            pred = np.append(pred, predicted_value)


        predict.append({"date":str(date),"prediction":predicted_value[0]})
        if(data_type == "hist"):
            date = date + timedelta(days=1)
        else:
            date = date + timedelta(minutes=1)





        d = {'$close':[testd[0,20],predicted_value]}
        new_df = pd.DataFrame(d)
        new_df.columns = ['close']
        new_df = getReturns(new_df,symbol)
        columns = new_df.columns
        close = columns[-2]
        returns = columns[-1]
        addFeatures(new_df,close, returns, 1)
        #print(new_df.shape)


        temptest = np.array(testd[0,5:25])
        for j in range(0,5):
            temptest = np.append(temptest,new_df.iloc[1][j])

        temptest = temptest.reshape(1,25)

        Testdata = np.append(Testdata,np.array(temptest), axis =0)

    return predict
