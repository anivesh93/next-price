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

# get stock name
def get_name(symbol):
    query = 'SELECT name FROM stock WHERE symbol="{0}";';
    return select(query.format(symbol))


# return all stocks with the latest realtime price
def get_stocks_realtime():
    query = '''
        SELECT realtime.symbol, stock.name, printf("%.2f", MAX(realtime.price)) 
        FROM realtime, stock
        WHERE realtime.symbol = stock.symbol
        GROUP BY realtime.symbol;
    '''
    return select(query)

# get the highest stock price of any company in the last ten days
def get_highest_ten_days(symbol):
    date_10 = datetime.now() - timedelta(days=10)
    date_output_format = '%Y-%m-%d'
    date_output = date_10.strftime(date_output_format)

    query = '''
        SELECT date, printf("%.2f", MAX(close)) 
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
        SELECT printf("%.2f", AVG(close)) 
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
        SELECT date, printf("%.2f", MIN(close)) 
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
    SELECT h.symbol AS sym, s.name, printf("%.2f", AVG(h.close))
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

def main():
    get_stocks_realtime()

if __name__ == '__main__':
    main()
