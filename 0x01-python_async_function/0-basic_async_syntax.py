#!/usr/bin/python3

# Import the necessary modules
# asyncio is a library to write single-threaded
#  concurrent code using coroutines, multiplexing I/O access over sockets
# and other resources, and implementing network clients and servers
import asyncio
# Import the random module to generate random numbers
import random


# Define an asynchronous function wait_random that waits for a random delay
# The function takes an optional parameter max_delay with a default value of 10
async def wait_random(max_delay=10):
    # Generate a random delay between 0 and max_delay
    delay = random.uniform(0, max_delay)
    # Wait for the generated delay using asyncio.sleep
    await asyncio.sleep(delay)
    # Return the delay value
    return delay
