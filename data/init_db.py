# written by: Mayank
# assisted by: Shreyas
# debugged by: Ashish

import sqlite3 as sql


# get all the queries from the db_commands.txt file
def get_queries():
    with open('db_commands.txt', 'r') as q_file:
        content = q_file.read()
    return content.strip()

def main():

    # open the connection to the database
    conn = sql.connect('stocks.db')
    cursor = conn.cursor()

    # execute all the queries that are present in the db_commands.txt file
    cursor.executescript(rget_queries())
    
    # commit and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
