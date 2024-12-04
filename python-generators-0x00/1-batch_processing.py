stream_users = __import__('0-stream_users').stream_users
import mysql.connector

def stream_users_in_batches(batch_size):
    """Stream users in batches."""
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'bece2018',
        'database': 'ALX_prodev'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM user_data')
        while True:
            batch = cursor.fetchmany(size=batch_size)
            if not batch:
                break
            yield batch
    finally:
        cursor.close()
        connection.close()
   

def batch_processing(batch_size):
    """Process batches of users."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] >= 25:
                yield(user)
            
            return user