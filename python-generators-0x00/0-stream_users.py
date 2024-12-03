#!/usr/bin/python3
#stream_users.py using generators(SQL) to stream data from a database
import mysql.connector

def stream_users(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user_data')
    for row in cursor:
        yield row
    cursor.close()
    connection.close()