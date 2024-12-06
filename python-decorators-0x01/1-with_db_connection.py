import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open the database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the original function
            # and include any other arguments that were passed
            result = func(conn, *args, **kwargs)
            # Commit any changes
            conn.commit()
            return result
        except Exception as e:
            # Rollback in case of any errors
            conn.rollback()
            raise
        finally:
            # Ensure the connection is always closed
            conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=1)
print(user)