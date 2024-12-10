import mysql.connector


class ExecuteQuery:
    def __init__(self, db_name, db_user, db_password, query):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.query = query

    
    def __enter__(self):
        self.connection = mysql.connector.connect(
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query)
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        if exc_type is not None:
            return False
        return True
    
with ExecuteQuery('alxProDev', 'root', 'bece2018', 'SELECT * FROM users WHERE age > 25') as cursor:
    for user in cursor.fetchall():
        print(user)