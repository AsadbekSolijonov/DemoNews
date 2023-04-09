import asyncio
import datetime
import logging

from api.weather_api import WeatherApiNews
from loader import db, bot

"""
Algorithm for sending weather news every hour 
"""


async def lat_lon_none(chat_id):
    datas = await db.select_lat_lon(chat_id)
    lat, lon = datas['lat'], datas['lon']
    return lat, lon


async def weather_text(lat, lon, chat_id):
    if not (lat and lon):
        coord = await lat_lon_none(chat_id)
        lat, lon = coord

    # Response from Weather API
    ####################################################
    if lat and lon:
        weather_response = WeatherApiNews(lon=lon, lat=lat)
        # Place name
        place_name = weather_response.place_name
        sys_info = weather_response.sys_info
        main = weather_response.main
        weather = weather_response.weather
        wind = weather_response.wind
        rain = weather_response.rain
        snow = weather_response.snow
        clouds = weather_response.clouds
        # time_zone = weather_response.response['timezone']
        ###################################################
        # Text
        text = [f"🌤 Weather | 🌤 Weather | 🌤 ",
                f"📍 Location {place_name} ",
                # f"Timezone: {datetime.datetime.fromtimestamp(time_zone).strftime('%H:%M')}",
                f"Country: {sys_info['country']}",
                f"Sunrise: {datetime.datetime.fromtimestamp(sys_info['sunrise']).strftime('%H:%M')}",
                f"Sunset: {datetime.datetime.fromtimestamp(sys_info['sunset']).strftime('%H:%M')}",
                f"Description: {', '.join([weather[index]['description'] for index in range(len(weather))])}",
                f"Clouds: {clouds['all']} %",
                f"Main: {', '.join([weather[index]['main'] for index in range(len(weather))])}",
                f"Temperature: {round(main['temp'] - 273.15, 0)} °С",
                f"Humidity: {main['humidity']} %",
                f"Wind Speed: {wind['speed']} m/s"
                f"{f'Snow: {snow}' if snow else ''}"
                f"{f'Rain: {rain}' if rain else ''}",
                ]
        text_f = '\n'.join(text)

        return text_f


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
                text = await weather_text(lat=None, lon=None, chat_id=user_id)
                text = f"🌤 News | 🌤 News | 🌤 News |\n\n{text}"
                # Message
                await bot.send_message(chat_id=user_id, text=text)


async def update_weather_news():
    # Infinite
    while True:
        # Running Function
        await send_weather_news()
        # AsyncIo Sleep 1 minute and Wake up
        await asyncio.sleep(60 - datetime.datetime.now().second)
