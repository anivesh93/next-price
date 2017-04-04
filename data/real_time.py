import urllib2
import sqlite3
from datetime import datetime
import time

stock_symbols = ['GOOGL', 'YHOO', 'MSFT', 'AMZN', 'TWTR', \
        'FB', 'CSCO', 'BAC', 'AAPL', 'AMD']
interval = 60

# create table
def create_table(conn, cursor):
    query = '''CREATE TABLE IF NOT EXISTS realtime
                (symbol text, price real, date text, time text, volume integer)'''
    cursor.execute(query)
    conn.commit()

# download one set of data for all symbols for one time step
def download_one(conn, cursor):

    # set up some variables
    url = r'http://finance.yahoo.com/d/quotes.csv?s={0}&f={1}'
    response_format = 'sl1d1t1v'
    datetime_input_format = '"%m/%d/%Y","%I:%M%p"'
    date_output_format = '%Y-%m-%d'
    time_output_format = '%H:%M'
    insert_query = 'INSERT INTO realtime VALUES ({0}, {1}, "{2}", "{3}", {4})'
    time_open, time_close = '09:30', '16:00'

    write_flag = False
    stock_time = ''

    # query the API
    try:
        response = urllib2.urlopen(url.format('+'.join(stock_symbols), response_format))
    except Exception as e:
        print e
        return

    # read the response and write into database
    for line in response:
        line = line.strip().split(',')
        date = datetime.strptime(','.join(line[2:4]), datetime_input_format)

        date_output = date.strftime(date_output_format)
        time_output = date.strftime(time_output_format)
        stock_time = time_output

        # filter proper times
        if time_open < time_output < time_close:
            cursor.execute(insert_query.format(
                line[0], line[1], date_output, time_output, line[4]))
            write_flag = True

    if write_flag:
        conn.commit()
        print datetime.now(), 'stock written for stock_time', stock_time
    else:
        print datetime.now(), 'stock skipped for stock_time', stock_time

def main():

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()
    #create_table(conn, cursor)
    
    while True:
        sleep_time = interval - time.time() % interval
        print datetime.now(), 'sleep_time', sleep_time
        time.sleep(sleep_time)
        download_one(conn, cursor)

if __name__ == '__main__':
    main()
