import aiosqlite

DB_NAME = "database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0,
            mining_speed REAL DEFAULT 0.001,
            last_claim INTEGER DEFAULT 0,
            ref_by INTEGER DEFAULT 0
        )
        """)

        await db.commit()


async def add_user(user_id, ref_by=0):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )

        user = await cursor.fetchone()

        if not user:
            await db.execute(
                "INSERT INTO users (user_id, ref_by) VALUES (?, ?)",
                (user_id, ref_by)
            )

            await db.commit()


async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )

        return await cursor.fetchone()


async def update_balance(user_id, balance):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "UPDATE users SET balance=? WHERE user_id=?",
            (balance, user_id)
        )

        await db.commit()
