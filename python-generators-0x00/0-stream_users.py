import mysql.connector

def stream_users():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'bece2018',
        'database': 'ALX_prodev'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)  # Use `dictionary=True` for easier access to column values
    try:
        cursor.execute('SELECT * FROM user_data')
        for row in cursor:
            yield row  # Yields rows one at a time
    finally:
        cursor.close()
        connection.close()
