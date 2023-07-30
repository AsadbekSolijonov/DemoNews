import logging
import hashlib
import asyncpg

from loader import dp, db
from aiogram import types
from datetime import datetime
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.phone import put_phone_keyboard
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # Changing from datetime to the Weekday by strftime method
    today = datetime.now().strftime('%A')

    try:
        # Add new user to Database
        await db.add_user(chat_id=message.chat.id,
                          fullname=message.from_user.full_name,
                          username=message.from_user.username,
                          phone_number=None)
        # phone_number
        user_phone = None
    except asyncpg.UniqueViolationError:
        # taking phone_number from database by chat_id
        db_phone = await db.user_phone(chat_id=message.chat.id)
        # hash256 phone_number
        user_phone = db_phone['phone_number']

    # Sending Sticker
    await message.answer_sticker(sticker='CAACAgIAAxkBAAGu7-VkMHjLOwldl2rsz4rz4jNGE7-adAAC0QADUomRI4TjSsB06wL9LwQ')
    # Text
    text = (f"👋 Today is {today}",
            f"🤗 Welcome, {message.from_user.full_name}!")
    if user_phone:
        # Send Message
        await message.answer(text='\n'.join(text))
    else:
        # This is keyboard for Sharing phone number
        keyboard = put_phone_keyboard()
        # Send Message
        await message.answer(text='\n'.join(text), reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def phone_handler(message: types.Message):
    # User chat id
    user_id = message.chat.id
    # Week day
    today = datetime.now().strftime('%A')
    # hashing phone_number
    hash_phone = hashlib.sha256(message.contact.phone_number.encode()).hexdigest()
    # Saving hashed phone_number to Database
    await db.update_phone(chat_id=message.chat.id, phone_number=hash_phone)
    # taking weather_time field from Database by user_id
    current_weather_time = await db.select_weather_time(chat_id=user_id)
    # Parsing time
    just_time = str(current_weather_time['weather_time'])[:5]
    # Text
    text = ('☺️ Thank you for your phone number\n',
            "🤖 Commands:",
            "/start - Start the bot",
            "/help - Help",
            "/current_weather - Current weather data",
            "/setting_weather_time - Setting the weather time\n",
            "🤔 If you want to change the WEATHER time, resend the correct time.",
            f"👋 Today is {today}",
            f"🕔 Weather updates come daily at {just_time}")
    # Send Message
    await message.answer(text='\n'.join(text), reply_markup=ReplyKeyboardRemove())
