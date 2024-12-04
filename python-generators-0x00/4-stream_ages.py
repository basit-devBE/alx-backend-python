import mysql.connector

def stream_user_age():
    """Stream user ages and calculate the average age from the database."""
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'bece2018',
        'database': 'ALX_prodev'
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT age FROM user_data')
        total_age = 0
        count = 0

        for row in cursor:
            age = row['age']
            total_age += age
            count += 1
            yield age  # Stream each age as a generator
        
        # After streaming, calculate and print the average
        average_age = total_age / count if count > 0 else 0
        print(f"Average age: {average_age:.2f}")
    finally:
        cursor.close()
        conn.close()

