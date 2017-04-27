from yahoo_finance import Share
from pprint import pprint
from datetime import datetime

import sqlite3

stock_symbols = ['GOOGL', 'YHOO', 'MSFT', 'AMZN', 'TWTR', \
        'FB', 'CSCO', 'BAC', 'AAPL', 'AMD']

def insert_data(symbol, prefix=""):
    conn = sqlite3.connect(prefix + 'stocks.db')
    cursor = conn.cursor()
    insert_query = \
        'INSERT INTO historical VALUES ("{0}", "{1}", {2}, {3}, {4}, {5}, {6})'
        
    print 'getting data for', symbol

    date_output_format = '%Y-%m-%d'
    date_output = datetime.now().strftime(date_output_format)

    stock = Share(symbol)
    data = stock.get_historical('2014-01-01', date_output)
    
    path = 'data/hist_' + symbol + '.csv'
    for day_data in data:
        try:
            cursor.execute(insert_query.format(
                symbol,
                day_data['Date'],
                day_data['Open'],
                day_data['High'],
                day_data['Low'],
                day_data['Close'],
                day_data['Volume']))
        except Exception as e:
            print e
            print 'insert failed for', symbol, day_data['Date']
            
    conn.commit()
    conn.close()


def main():
    for symbol in stock_symbols:
        insert_data(symbol)

if __name__ == '__main__':
    main()
