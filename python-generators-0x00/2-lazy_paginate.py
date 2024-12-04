#using python generator to lazy paginate
# The goal is to not have the full list in memory, but to only have the correct page of users at a time.
import mysql.connector
def lazy_paginate(page_size):
    dbConfig ={
        'host': 'localhost',
        'user': 'root',
        'password': 'bece2018',
        'database': 'ALX_prodev'
   }
    conn = mysql.connector.connect(**dbConfig)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_data')
        while True:
            page = cursor.fetchmany(size=page_size)
            if not page:
                break
            yield page
    finally:
        cursor.close()
        conn.close()