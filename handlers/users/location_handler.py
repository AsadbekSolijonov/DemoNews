from aiogram import types

from keyboards.default.location import put_location_keyboard
from loader import dp, db
from api.weather_api import WeatherApiNews
from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove)


@dp.message_handler(commands=['current_weather'])
async def location_command(message: types.Message):
    # Text
    text = ("Share your location 📍",
            "and the same time every day",
            "be aware of the weather information",)
    text = '\n'.join(text)
    # This Keyboard for Sending User's current Location
    location_keyboard = put_location_keyboard()
    # Send Message
    await message.answer(text=text, reply_markup=location_keyboard)


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
    text = await WeatherApiNews.weather_text(lat, lon, chat_id=user_id)
    # Send Message
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
