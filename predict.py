from __future__ import print_function
from helper_func import addFeatures, performRegression, getStock, getRealTime
import sys
import os
import pickle
import traceback
import numpy as np

def main(symbol, data_type, output_dir):

    scores = {}

    maxdelta = 30

    delta = range(8, maxdelta)
    print('Delta days accounted: ', max(delta))

    #stock_symbols = ['GOOGL','YHOO', 'MSFT', 'TWTR', 'FB', 'CSCO', 'BAC', 'AAPL', 'AMD']
    #stock_symbols = ['AMZN']
    stock_symbols = [symbol]

    for symbol in stock_symbols:
        try:

            if(data_type == "hist"):
                dataset = getStock(symbol, '2015-01-01', '2017-04-24')
            else:
                dataset = getRealTime(symbol)


            #apply roll mean delayed returns
            # Add features
            columns = dataset.columns
            close = columns[-2]
            returns = columns[-1]


            #for dele in delta:
            addFeatures(dataset, close, returns, 1)



            finance = dataset.iloc[1:,:] # computation of returns and moving means introduces NaN which are nor removed

            #print(finance)
            previ = 2
            Traindata = np.array(dataset.ix[1:6,:].as_matrix().reshape(1,25))

            Trainlabel = np.array(finance['Close_%s' %symbol][6])

            for i in range(7,finance.shape[0]):
                tempdata = np.array(dataset.ix[previ:i,:].as_matrix().reshape(1,25))
                Traindata = np.concatenate((Traindata, tempdata) ,axis=0)
                #print(tempdata)
                previ = previ+1

                templabel = np.array(finance['Close_%s' %symbol][i])
                Trainlabel = np.append(Trainlabel,templabel)

            print(Traindata.shape)
            print(Trainlabel.shape)

            if 'symbol' in finance.columns:
                finance.drop('symbol', axis=1, inplace=True)

            mean_squared_errors, r2_scores = performRegression(Traindata,Trainlabel, 0.95, symbol, output_dir, data_type)

            scores[symbol] = [mean_squared_errors, r2_scores]

        except Exception, e:
            pass
            traceback.print_exc()

    with open(os.path.join(output_dir, 'scores.pickle'), 'wb') as handle:
        pickle.dump(scores, handle)

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2], sys.argv[3])
