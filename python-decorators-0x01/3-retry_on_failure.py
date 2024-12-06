import time
import sqlite3 
import functools
import random

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

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(retries):
                try:
                    # Attempt to execute the function
                    return func(*args, **kwargs)
                except Exception as e:
                    # Store the last exception
                    last_exception = e
                    
                    # Print retry attempt information
                    print(f"Attempt {attempt + 1} failed: {e}")
                    
                    # Wait before retrying (with some jitter to prevent thundering herd)
                    wait_time = delay * (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
            
            # If all retries fail, raise the last exception
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)