import sqlite3 as sql

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
    query = 'SELECT symbol, MAX(price) FROM realtime GROUP BY symbol';
    return select(query)

def main():
    get_stocks_realtime()

if __name__ == '__main__':
    main()
