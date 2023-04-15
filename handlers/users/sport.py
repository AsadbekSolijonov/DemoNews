import asyncio
import datetime

from loader import db, bot
from api.sport_api import SportApiNews


async def send_sport_news(text):
    # (chat_id, weather_time) but we need not weather_time field
    datas = await db.chat_id_time_users()

    for user_id, _ in datas:
        # Text
        text = f'⛳️ Sport News\n\n{text.__next__()}'
        # Send Message
        await bot.send_message(chat_id=user_id, text=text)


async def update_sport_news():
    # Infinite
    # Text
    text = SportApiNews().yield_text
    while True:
        # Running Function
        await send_sport_news(text)
        # Time
        datetime_ = datetime.datetime.now()
        min_ = datetime_.minute
        sec_ = datetime_.second
        # AsyncIO Sleep 1 hour and wake up
        await asyncio.sleep(3600 - ((min_ * 60) + sec_))
        # await asyncio.sleep(5)
