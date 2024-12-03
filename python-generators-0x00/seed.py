import mysql.connector
import csv

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'bece2018'
}

def connect_db():
    return mysql.connector.connect(**db_config)

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS ALX_prodev')
    cursor.close()

def connect_to_prodev():
    db_config['database'] = 'ALX_prodev'
    return mysql.connector.connect(**db_config)

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY, 
            name VARCHAR(50) NOT NULL, 
            email VARCHAR(100) NOT NULL, 
            age DECIMAL NOT NULL
        )
    ''')
    cursor.close()
    connection.commit()

def insert_data(connection,data):
    cursor = connection.cursor()
    with open(data, 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)
        for row in csv_data:
            cursor.execute('''
                INSERT INTO user_data (user_id, name, email, age) 
                VALUES (%s, %s, %s, %s)
            ''', row)
    connection.commit()
    cursor.close()
