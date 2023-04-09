import asyncpg
from typing import Union
from asyncpg.pool import Pool
from asyncpg import Connection
from data import config


class PostgreSQLConnection:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def connect_pool(self):
        self.pool = await asyncpg.create_pool(
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )

    async def execute(self, sql_command, *args, fetch: bool = False, fetchrow: bool = False, fetchval: bool = False,
                      execute: bool = True):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(sql_command, *args)
                elif fetchval:
                    result = await connection.fetchrow(sql_command, *args)
                elif fetchrow:
                    result = await connection.fetchval(sql_command, *args)
                elif execute:
                    result = await connection.execute(sql_command, *args)

            return result

    async def create_table_users(self):
        sql_command = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        chat_id BIGINT NOT NULL UNIQUE,
        fullname VARCHAR(128) NOT NULL,
        username VARCHAR(128) NULL,
        phone_number VARCHAR(64) NULL,
        weather_time TIME DEFAULT '09:00:00',
        lat REAL DEFAULT 41.2995,
        lon REAL DEFAULT 69.2401)
        """
        await self.execute(sql_command, execute=True)

    async def add_user(self, chat_id, fullname, username, phone_number):
        sql_command = """
        INSERT INTO Users (chat_id, fullname, username, phone_number) VALUES ($1, $2, $3, $4) returning *
        """
        return await self.execute(sql_command, chat_id, fullname, username, phone_number, fetchrow=True)

    async def update_weather_time(self, time, user_id):
        sql_command = """
        UPDATE Users SET weather_time=$1 WHERE chat_id=$2 
        """
        return await self.execute(sql_command, time, user_id, execute=True)

    async def update_lat_lon(self, lat, lon, chat_id):
        sql_command = """
        UPDATE Users SET lat=$1, lon=$2 WHERE chat_id=$3
        """
        return await self.execute(sql_command, lat, lon, chat_id, execute=True)

    async def update_phone(self, phone_number, chat_id):
        sql_command = """
        UPDATE Users SET phone_number=$1 WHERE chat_id=$2
        """
        return await self.execute(sql_command, phone_number, chat_id, execute=True)

    async def select_weather_time(self, chat_id):
        sql_command = """
        SELECT weather_time FROM Users WHERE chat_id=$1
        """
        return await self.execute(sql_command, chat_id, fetchval=True)

    async def chat_id_time_users(self):
        sql_command = """
        SELECT chat_id, weather_time FROM Users
        """
        return await self.execute(sql_command, fetch=True)

    async def select_lat_lon(self, chat_id):
        sql_command = """
        SELECT lat, lon FROM Users WHERE chat_id=$1
        """
        return await self.execute(sql_command, chat_id, fetchval=True)

    async def update_lat_lon(self,lat, lon, chat_id):
        sql_command = """
        UPDATE Users SET lat=$1, lon=$2 WHERE chat_id=$3
        """
        return await self.execute(sql_command, lat, lon, chat_id, fetchval=True)

    async def user_phone(self, chat_id):
        sql_command = """
        SELECT phone_number FROM Users WHERE chat_id=$1
        """
        return await self.execute(sql_command, chat_id, fetchval=True)

    async def drop_table(self):
        sql_command = """
        DROP TABLE Users
        """
        return await self.execute(sql_command, execute=True)
