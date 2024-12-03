#!/usr/bin/python3
from itertools import islice
from 0-stream_users.py import stream_users
# Iterate over the generator function and print only the first 6 rows
for user in islice(stream_users(), 6):
    print(user)
