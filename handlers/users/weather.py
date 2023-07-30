import asyncio
import datetime
import logging

from api.weather_api import WeatherApiNews
from loader import db, bot

"""
Algorithm for sending weather news every hour 
"""


async def send_weather_news():
    # (chat_id, weather_time)
    datas = await db.chat_id_time_users()
    if datas:
        # Real time
        now = datetime.datetime.now()
        for user_id, oclock in datas:
            # Is Database time equal to Real time?
            if now.hour == oclock.hour and now.minute == oclock.minute:
                # The Weather Text
                text = await WeatherApiNews.weather_text(lat=None, lon=None, chat_id=user_id)
                text = f"🌤 News | 🌤 News | 🌤 News |\n\n{text}"
                # Send Message
                await bot.send_message(chat_id=user_id, text=text)


async def update_weather_news():
    # Infinite
    while True:
        # Running Function
        await send_weather_news()
        # AsyncIo Sleep 1 minute and Wake up
        await asyncio.sleep(60 - datetime.datetime.now().second)
