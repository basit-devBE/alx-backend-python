```
import asyncio

async def main():
    print('Hello...')
    await asyncio.sleep(1)
    print('... World!')

# Python 3.7+
asyncio.run(main())

# Python 3.6
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()
