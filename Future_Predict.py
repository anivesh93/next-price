from __future__ import print_function
from helper_func import addFeatures, performRegression, getStock,futurepredict, getRealTimePredict
import sys
import os
import pickle
import traceback
import numpy as np
from datetime import  timedelta, date, datetime


#Call this function as folllows
# For Historical predictStock("GOOGL", "2017-04-21 ", "hist")\
# For Real predictStock("GOOGL", "2017-04-21 ", "real")

def predictStock(symbol, dt, data_type):

    """

    :rtype: object
    """
    if(data_type == "hist"):
        d = date(int(dt.split("-")[0]), int(dt.split("-")[1]), int(dt.split("-")[2]))
        startdate = d - timedelta(days=15)
        enddate = d

    scores = {}

    maxdelta = 30

    delta = range(8, maxdelta)
    #print('Delta days accounted: ', max(delta))

    if(data_type == "hist"):
        dataset = getStock(symbol)
    else:
        dataset, dt = getRealTimePredict(symbol)

        d = datetime(int(dt.split("-")[0]), int(dt.split("-")[1]), int(dt.split("-")[2].split(" ")[0]), int(dt.split("-")[2].split(" ")[1].split(":")[0]),
                     int(dt.split("-")[2].split(" ")[1].split(":")[1]))
        startdate = d - timedelta(minutes=15)
        enddate = d


    #apply roll mean delayed returns
    # Add features
    columns = dataset.columns
    close = columns[-2]
    returns = columns[-1]


    #for dele in delta:
    addFeatures(dataset, close, returns, 1)


    finance = dataset.iloc[1:,:] # computation of returns and moving means introduces NaN which are nor removed

    previ = 2
    Traindata = np.array(dataset.ix[1:6,:].as_matrix().reshape(1,25))

    Trainlabel = np.array(finance['Close_%s' %symbol][6])

    for i in range(7,finance.shape[0]):
        tempdata = np.array(dataset.ix[previ:i,:].as_matrix().reshape(1,25))
        Traindata = np.concatenate((Traindata, tempdata) ,axis=0)
        previ = previ+1

        templabel = np.array(finance['Close_%s' %symbol][i])
        Trainlabel = np.append(Trainlabel,templabel)


    if 'symbol' in finance.columns:
        finance.drop('symbol', axis=1, inplace=True)
    '''
    RandomForest Regressor
    SVR
    Bagging Regressor
    AdaBoost Regressor
    KNeighbors Regressor
    GradientBoosting Regressor
    MLPClassifier
    '''
    model_name = "RandomForest Regressor"
    predictedStock = futurepredict(Traindata,Trainlabel, symbol, startdate,model_name,data_type)

    return predictedStock


