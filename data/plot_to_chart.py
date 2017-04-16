import sqlite3
import json

def main():

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM historical LIMIT 50')
    rows = cursor.fetchall()
    
    cleaned = []
    ctr = 1

    for row in rows:
        # print row[4], row[5]
        temp = {}
        temp["closePrice"]  = row[4]
        temp["date"] = row[5]
        cleaned.append(temp)
        ctr += 1

    for row in cleaned:
        print row
    
    conn.close()

    fp = open('data.json', 'wb')
    json.dump(cleaned, fp, indent = 3)

if __name__ == '__main__':
    main()
