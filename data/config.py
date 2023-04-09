from environs import Env

# using from environs
env = Env()
env.read_env()

# Reading datas from .env file
# Bot
BOT_TOKEN = env.str("BOT_TOKEN")  # BOT TOKEN
ADMINS = env.list("ADMINS")  # admins list
IP = env.str("ip")  # host api address

# Postgresql
DB_USER = env.str('DB_USER')
DB_NAME = env.str('DB_NAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.str('DB_PORT')

# API KEYS
CURR_WEATHER_API_KEY = env.str('CURR_WEATHER_API_KEY')
SPORT_API_KEY = env.str('SPORT_API_KEY')
