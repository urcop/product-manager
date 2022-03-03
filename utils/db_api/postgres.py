import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Pool = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_NAME,
            password=config.DB_PASS,
            host=config.IP,
            database=config.db
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connect:
            connect: Connection
            async with connect.transaction():
                if fetch:
                    result = await connect.fetch(command, *args)
                elif fetchval:
                    result = await connect.fetchval(command, *args)
                elif fetchrow:
                    result = await connect.fetchrow(command, *args)
                elif execute:
                    result = await connect.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                username VARCHAR(255) DEFAULT NULL,
                telegram_id BIGINT NOT NULL UNIQUE,
                is_admin BOOLEAN NOT NULL DEFAULT FALSE
            )
        """
        await self.execute(sql, execute=True)

    async def add_user(self, fullname, username, telegram_id):
        sql = """
            INSERT INTO users (fullname, username, telegram_id) VALUES ($1, $2, $3) returning *
        """
        return await self.execute(sql, fullname, username, telegram_id, execute=True)

    async def select_user(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def add_admin(self, telegram_id):
        sql = "UPDATE users SET is_admin=$1 WHERE telegram_id=$2"
        return await self.execute(sql, telegram_id, execute=True)

    async def is_admin(self, telegram_id):
        sql = "SELECT is_admin FROM users WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchval=True)
