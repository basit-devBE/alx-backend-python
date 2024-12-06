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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Start the transaction by disabling autocommit
            conn.execute('BEGIN')
            
            # Execute the original function
            result = func(conn, *args, **kwargs)
            
            # If no exception, commit the transaction
            conn.commit()
            
            return result
        except Exception as e:
            # If an exception occurs, rollback the transaction
            conn.rollback()
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')