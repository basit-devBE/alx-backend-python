stream_users = __import__('0-stream_users').stream_users

def stream_users_in_batches(batch_size):
    """Stream users in batches."""
    batch = []
    for user in stream_users():  # Assuming stream_users() fetches user data one at a time
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []  # Reset batch after yielding
    if batch:  # Yield any remaining users
        yield batch

def batch_processing(batch_size):
    """Filters users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
