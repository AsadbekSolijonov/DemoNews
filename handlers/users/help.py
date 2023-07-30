from loader import dp
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    # Text
    text = ("🤖 Commands: ",
            "/start - Start the bot",
            "/help - Help",
            "/setting_weather_time - Setting the weather time",
            "/current_weather - Current weather data")
    # Send Message
    await message.answer("\n".join(text))
