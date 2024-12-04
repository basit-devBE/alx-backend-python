import mysql.connector
#use python generate to aggregate the average age of users in the database
def stream_user_age():
    dbConfig = {
        'host': 'localhost',
        'user': 'root',
        'password': 'bece2018',
        'database': 'ALX_prodev'
    }
    conn = mysql.connector.connect(**dbConfig)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT age FROM user_data')
        for row in cursor:
            yield row.age
    finally:
        cursor.close()
        conn.close()