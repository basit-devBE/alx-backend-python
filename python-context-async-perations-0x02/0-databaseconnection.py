import mysql.connector

class DatabaseConnection:
    def __init__(self, db_name, db_user, db_password):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
    
    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


with DatabaseConnection('alxProDev', 'root', 'bece2018') as connection:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()  # Use fetchall() to retrieve results
    for user in users:
        print(user)
