import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('alxProDev.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE age > 25')
        users = await cursor.fetchall()
        return users

async def async_fetch_older_users():
    async with aiosqlite.connect('alxProDev.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE age > 40')
        older_users = await cursor.fetchall()
        return older_users

async def fetch_concurrently():
    # Run both queries concurrently
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("Users older than 25:")
    print(users)
    print("\nUsers older than 40:")
    print(older_users)

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
