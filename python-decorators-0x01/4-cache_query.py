import time
import sqlite3 
import functools

query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already in the cache
        if query in query_cache:
            print("Returning cached result")
            return query_cache[query]
        
        # If not in cache, execute the query
        result = func(conn, query, *args, **kwargs)
        
        # Cache the result
        query_cache[query] = result
        
        return result
    
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")