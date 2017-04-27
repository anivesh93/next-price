import sqlite3 as sql
import random
from datetime import datetime, timedelta

# execute a select statement query on stocks db and return all results
def select(query):
    conn = sql.connect('data/stocks.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return data

def update(query):
    conn = sql.connect('data/stocks.db')
    cursor = conn.cursor()
    try: 
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print e
    conn.close()

def insert_stock(symbol, name):
    query = 'INSERT INTO stock values ("{0}", "{1}");'
    update(query.format(symbol, name))

# get stock name
def get_name(symbol):
    query = 'SELECT name FROM stock WHERE symbol="{0}";';
    return select(query.format(symbol))

def get_stocks():
    query = 'SELECT * FROM stock;'
    return select(query)

# return all stocks with the latest realtime price
def get_stocks_realtime():
    query = '''
        SELECT stock.symbol, stock.name, ROUND(MAX(realtime.price), 2) 
        FROM realtime, stock
        WHERE realtime.symbol = stock.symbol
        GROUP BY stock.symbol;
    '''
    return select(query)

# get the highest stock price of any company in the last ten days
def get_highest_ten_days(symbol):
    date_10 = datetime.now() - timedelta(days=10)
    date_output_format = '%Y-%m-%d'
    date_output = date_10.strftime(date_output_format)

    query = '''
        SELECT date, ROUND(MAX(close), 2) 
        FROM historical 
        WHERE date > "{0}" AND symbol = "{1}";
    '''
    return select(query.format(date_output, symbol))

# average stock price of any company in the latest one year
def get_average_one_year(symbol):
    date_1_year = datetime.now() - timedelta(days=365)
    date_output_format = '%Y-%m-%d'
    date_output = date_1_year.strftime(date_output_format)

    query = '''
        SELECT ROUND(AVG(close), 2) 
        FROM historical 
        WHERE date > "{0}" AND symbol = "{1}";
    '''
    return select(query.format(date_output, symbol))

# get the lowest stock price of any company in the last one year
def get_lowest_one_year(symbol):
    date_1_year = datetime.now() - timedelta(days=365)
    date_output_format = '%Y-%m-%d'
    date_output = date_1_year.strftime(date_output_format)

    query = '''
        SELECT date, ROUND(MIN(close), 2) 
        FROM historical 
        WHERE date > "{0}" AND symbol = "{1}";
    '''
    return select(query.format(date_output, symbol))


# list the ids of companies along with their name who have the 
# average stock price lesser than the lowest of any of the Selected Company 
# in the latest one year
def get_avg_low(symbol):
    date_1_year = datetime.now() - timedelta(days=365)
    date_output_format = '%Y-%m-%d'
    date_output = date_1_year.strftime(date_output_format)

    query = '''
    SELECT h.symbol AS sym, s.name, ROUND(AVG(h.close), 2)
    FROM historical as h, stock as s 
    WHERE (
        SELECT AVG(close) 
        FROM historical 
        WHERE symbol=sym
        ) < (
        SELECT MIN(close) 
        FROM historical 
        WHERE date > "{0}" AND symbol="{1}"
        ) 
        AND
        h.symbol = s.symbol
    GROUP BY h.symbol;
    '''

    return select(query.format(date_output, symbol))

# return the historical data for a symbol from 2015 onwards
def get_historical_records(symbol):
    query = '''
        SELECT * 
        FROM historical 
        WHERE SYMBOL = "{0}" AND DATE > '2015-01-01'
        -- ORDER BY DATE DESC
        -- LIMIT 20
    '''

    return select(query.format(symbol))

# return all available realtime data for a symbol
def get_realtime_records(symbol):
    query = '''
        SELECT * 
        FROM realtime 
        WHERE SYMBOL = "{0}" 
        -- ORDER BY date, time DESC
        -- LIMIT 15
    '''

    return select(query.format(symbol))

def get_realtime_15(symbol):
    query = '''
        SELECT * 
        FROM realtime 
        WHERE SYMBOL = "{0}" 
        ORDER BY date, time DESC
        LIMIT 15
    '''

    return select(query.format(symbol))

def main():
    get_stocks_realtime()

if __name__ == '__main__':
    main()
