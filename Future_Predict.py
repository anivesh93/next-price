from __future__ import print_function
from helper_func import addFeatures, performRegression, getStock,futurepredict
import sys
import os
import pickle
import traceback
import numpy as np
from datetime import  timedelta, date



def main(symbol,dt):

    d = date(int(dt.split("-")[0]), int(dt.split("-")[1]), int(dt.split("-")[2]))
    startdate = d - timedelta(days=15)
    enddate = d

    scores = {}

    maxdelta = 30

    delta = range(8, maxdelta)
    print('Delta days accounted: ', max(delta))


    dataset = getStock(symbol, startdate, enddate)

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

    predict = futurepredict(Traindata,Trainlabel, symbol, startdate)

    print(predict)



if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
