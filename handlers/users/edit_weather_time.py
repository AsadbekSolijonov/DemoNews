import re
import logging
from loader import dp, db
from aiogram import types
from datetime import datetime

from aiogram.dispatcher import FSMContext

from states.edit_weather_time import StateWeatherTime
from keyboards.inline.yes_no import yes_no


@dp.message_handler(commands=['setting_weather_time'])
async def edit_weather_time(message: types.Message):
    # User chat id
    user_id = message.chat.id
    # Taking the weather time value from database
    current_weather_time = await db.select_weather_time(chat_id=user_id)
    # Parsing time format time(00:00:00) to str(00:00)
    just_time = str(current_weather_time['weather_time'])[:5]
    # Text
    text = (f"👋 Today is {datetime.now().strftime('%A')}\n",
            "🌦 What time of day do you need weather information? ",
            "if you want to receive news, follow ",
            "write it down in the form and do it every day ",
            "we will send you an update in time.\n",
            "🕔 Time Format:",
            "09:00 - nine in the morning",
            "12:00 - Lunch Time",
            "21:00 - Nine in the evening",
            "00:00 - Midnight\n",
            f"🕔 Weather updates come daily at {just_time}",)
    text = '\n'.join(text)
    # Send Message
    await message.reply(text=text)

    # Statement
    await StateWeatherTime.weather_time.set()


async def check_time(message, state):
    # Regex Pattern
    pattern = r'^(?:[01]\d|2[0-3]):[0-5]\d$'
    # User chat id
    user_id = message.chat.id
    # Taking the weather time value from database
    current_weather_time = await db.select_weather_time(chat_id=user_id)
    # Parsing time format time(00:00:00) to str(00:00)
    just_time = str(current_weather_time['weather_time'])[:5]
    # Checking time by the regular Expression (Regex)
    if re.match(pattern, message.text):
        # Saving time value to FSMContext
        async with state.proxy() as data:
            data['time'] = message.text
        # Text
        text = (f'👋 Today is {datetime.now().strftime("%A")}',
                f'🕔 Weather updates come daily at {just_time}. But\n',
                f'🌦 Would you like to receive daily weather updates at {message.text} ?',)
        text = '\n'.join(text)
        # This is inline button `yes` and `no` for confirm time
        inline_keyboard = yes_no()
        # Send Message
        await message.reply(text=text, reply_markup=inline_keyboard)
        # Statement
        await StateWeatherTime.confirm.set()
    else:
        # Text
        text = (f"❌ I didn`t get it: \n",
                f"🤖 Commands:",
                f"/start - Start the bot",
                f"/help - Help",
                f"/setting_weather_time - Setting the weather time",
                f"/current_weather - Current weather data",
                f"🤔 If you want to change the WEATHER time, resend the correct time.\n",
                f"🕔 Weather updates come daily at {just_time}")
        text = '\n'.join(text)
        # Send Message
        await message.reply(text=text)
        # Statement finish
        await state.finish()


@dp.message_handler(state=StateWeatherTime.weather_time)
async def regex_time(message: types.Message, state: FSMContext):
    # Statement
    # checking the time format from (00:00) to (23:59)
    await check_time(message, state)


@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    # No Statement
    # Checking the time format from (00:00) to (23:59)
    await check_time(message, state)


@dp.callback_query_handler(text=['yes', 'no'], state=StateWeatherTime.confirm)
async def confirm_time(call: types.CallbackQuery, state: FSMContext):
    # Callback_data
    conf_data = call.data
    # User chat id
    user_id = call.message.chat.id
    # take time from database by user_id field
    current_weather_time = await db.select_weather_time(chat_id=user_id)
    # time format from (00:00:00) to (00:00)
    just_time = str(current_weather_time['weather_time'])[:5]
    # saving time value in FSMContext
    async with state.proxy() as data:
        text_time = data['time']

    if conf_data == 'yes':
        # Parsing from str(time) to datetime(time) and saving to database
        await db.update_weather_time(time=datetime.strptime(text_time, '%H:%M').time(), user_id=user_id)
        # Text
        alert_text = f"🕔 {text_time} saved!"
        # Send Alert Message
        await call.answer(text=alert_text, cache_time=60000)
        # Text
        message_text = f'🕔 {text_time} saved!'
        # Send Message
        await call.message.answer(text=message_text)

    elif conf_data == 'no':
        # Text
        alert_text = f"⚠️ {text_time} not save"
        # Send Alert Message
        await call.answer(text=alert_text, cache_time=60000)
        # Text
        message_text = f'⚠️ {text_time} didn`t save!'
        # Send Message
        await call.message.answer(text=message_text)
        # Text
        answer_text = (f"👋 Today is {datetime.now().strftime('%A')}",
                       f"🕔 Weather updates come daily at {just_time}")
        answer_text = '\n'.join(answer_text)
        # Send Message
        await call.message.answer(text=answer_text)
    # Statement finish
    await state.finish()
