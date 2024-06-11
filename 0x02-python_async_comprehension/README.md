```
Python Async Generators
=======================

**What are Async Generators?**
-----------------------------

```
async def my_generator():
    for i in range(10):
        yield i
```

**How to Use Async Generators**
-----------------------------

```
async def main():
    async for num in my_generator():
        print(num)

import asyncio
asyncio.run(main())
```

**Async Generator Example: Reading a File**
-----------------------------------------

```
async def read_file(filename):
    with open(filename, 'r') as f:
        async for line in f:
            yield line.strip()

async def main():
    async for line in read_file('example.txt'):
        print(line)

import asyncio
asyncio.run(main())
```

**Async Generator Example: Web Scraping**
-----------------------------------------

```
import aiohttp

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def scrape_website():
    async with aiohttp.ClientSession() as session:
        html = await fetch_page(session, 'https://example.com')
        yield html

async def main():
    async for html in scrape_website():
        print(html)

import asyncio
asyncio.run(main())
```

**Best Practices**
-----------------

```
# Avoid mixing sync and async code
def sync_function():
    #...

async def async_function():
    #...

# Use async generators with async for loops
async def my_generator():
    #...

async def main():
    async for item in my_generator():
        #...

# Use try/finally to ensure cleanup
async def my_generator():
    try:
        #...
    finally:
        #...
```

**Resources**
------------

* [Python Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
* [Async Generators Tutorial](https://www.python.org/dev/peps/pep-0525/)
* [Asyncio Best Practices](https://docs.python.org/3/library/asyncio-dev.html#asyncio-dev-best-practices)
