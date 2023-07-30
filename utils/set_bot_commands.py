from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start the bot"),
            types.BotCommand("help", "help"),
            types.BotCommand("setting_weather_time", "Setting the weather time"),
            types.BotCommand("current_weather", "Current weather data")
        ]
    )
