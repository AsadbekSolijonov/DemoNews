from aiogram.dispatcher.filters.state import State, StatesGroup


class StateWeatherTime(StatesGroup):
    weather_time = State()
    confirm = State()
