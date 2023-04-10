import asyncio

from aiogram import executor

from handlers.users.sport import update_sport_news
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.weather import update_weather_news


async def on_startup(dispatcher):
    #  db connection
    await db.connect_pool()
    # drop table
    await db.drop_table()
    # create table users if not exists
    await db.create_table_users()
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    # update weather news
    asyncio.ensure_future(update_weather_news())
    # update sport news
    asyncio.ensure_future(update_sport_news())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
