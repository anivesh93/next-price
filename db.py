import sqlite3 as sql
from datetime import datetime, timedelta

# execute a select statement query on stocks db and return all results
def select(query):
    conn = sql.connect('data/stocks.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    return data

# return all stocks with the latest realtime price
def get_stocks_realtime():
    query = 'SELECT symbol, printf("%.2f", MAX(price)) FROM realtime GROUP BY symbol';
    return select(query)

# get the highest stock price of any company in the last ten days
def get_highest_ten_days(symbol):
    date_10 = datetime.now() - timedelta(days=10)
    date_output_format = '%Y-%m-%d'
    date_output = date_10.strftime(date_output_format)

    query = 'SELECT date, MAX(close) FROM historical WHERE date > "' + \
            date_output + '" AND symbol = "' + symbol + '";'
    return select(query)

# average stock price of any company in the latest one year
def get_average_one_year(symbol):
    date_1_year = datetime.now() - timedelta(days=365)
    date_output_format = '%Y-%m-%d'
    date_output = date_1_year.strftime(date_output_format)

    query = 'SELECT AVG(close) FROM historical WHERE date > "' + \
            date_output + '" AND symbol = "' + symbol + '";'
    return select(query)

# get the lowest stock price of any company in the last one year
def get_lowest_one_year(symbol):
    date_1_year = datetime.now() - timedelta(days=365)
    date_output_format = '%Y-%m-%d'
    date_output = date_1_year.strftime(date_output_format)

    query = 'SELECT date, MIN(close) FROM historical WHERE date > "' + \
            date_output + '" AND symbol = "' + symbol + '";'
    return select(query)


def get_avg_low(symbol):
    date_1_year = datetime.now() - timedelta(days=365)
    date_output_format = '%Y-%m-%d'
    date_output = date_1_year.strftime(date_output_format)

    query = '''
    SELECT symbol AS sym, AVG(close) 
    FROM historical 
    WHERE (
        SELECT AVG(close) 
        FROM historical 
        WHERE symbol=sym
        ) < (
        SELECT MIN(close) 
        FROM historical 
        WHERE date > "{0}" AND symbol="{1}"
        ) 
    GROUP BY symbol
    '''

    return select(query.format(date_output, symbol))

def main():
    get_stocks_realtime()

if __name__ == '__main__':
    main()
