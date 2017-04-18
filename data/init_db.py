import sqlite3 as sql

def get_queries():
    with open('db_commands.txt', 'r') as q_file:
        content = q_file.read()
    return content.strip()

def main():

    conn = sql.connect('stocks.db')
    cursor = conn.cursor()

    cursor.executescript(get_queries())
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
