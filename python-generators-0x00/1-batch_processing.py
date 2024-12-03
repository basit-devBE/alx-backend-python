#generate and process data from the database in batches
stream_users = __import__('0-stream_users').stream_users
def stream_users_in_batches(batch_size):
    """Stream users in batches"""
    i = 0
    while i < batch_size:
        yield from stream_users()
        i += 1