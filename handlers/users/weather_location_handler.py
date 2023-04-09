import datetime

from api.weather_api import WeatherApiNews
from handlers.users.weath_send_news import send_weather_news, weather_text
from loader import dp, db, bot
from aiogram import types
from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove)


@dp.message_handler(commands=['current_weather'])
async def location_command(message: types.Message):
    # Text
    text = ("Share your location 📍",
            "and same time every day",
            "be aware of the weather information",)
    text = '\n'.join(text)
    # ReplyKeyboardMarkup for Send User's current Location
    location_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    loc_btn = KeyboardButton(text='Share your Location', request_location=True)
    share_location = location_btn.add(loc_btn)
    # Message
    await message.answer(text=text, reply_markup=share_location)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location_handler(message: types.Message):
    # User id
    user_id = message.chat.id
    # Receiving Coordinates lat and lon
    lat = message.location.latitude
    lon = message.location.longitude
    # Updating Database to new lat and lon by user id
    await db.update_lat_lon(lat=lat, lon=lon, chat_id=user_id)
    # Taking The Weather news Text
    text = await weather_text(lat, lon, chat_id=user_id)
    # Message
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
