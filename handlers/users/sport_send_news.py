import asyncio
import datetime

from loader import db, bot
from api.sport_api import SportApiNews


async def send_sport_news():
    # (chat_id, weather_time) but we need not weather_time field
    datas = await db.chat_id_time_users()
    text = SportApiNews().yield_text
    for user_id, _ in datas:
        # Text
        text = f'⛳️ Sport News\n\n{text.__next__()}'
        # Message
        await bot.send_message(chat_id=user_id, text=text)


async def update_sport_news():
    # Infinite
    while True:
        # Running Function
        await send_sport_news()
        # Time
        datetime_ = datetime.datetime.now()
        min_ = datetime_.minute
        sec_ = datetime_.second
        # AsyncIO Sleep 1 hour and wake up
        # await asyncio.sleep(3600 - ((min_ * 60) + sec_))
        await asyncio.sleep(5)
