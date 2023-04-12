import datetime
from pprint import pprint

from data import config
import requests
from api.api_decorator import try_except
from loader import db


class WeatherApiNews:
    """
    API Docs: https://openweathermap.org/current
    """

    def __init__(self, lat, lon):
        self.api_key = config.CURR_WEATHER_API_KEY
        self.lat = lat
        self.lon = lon
        self.url = None

    @property
    def request(self):
        """
        return API response
        """
        self.url = f'https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api_key}'
        result = requests.get(url=self.url).json()
        return result

    @property
    def response(self):
        """
        return property request() instance method
        """
        return self.request

    @property
    @try_except
    def place_name(self):
        """
        return Place Name
        """
        return self.response['name']

    @property
    @try_except
    def sys_info(self):
        """
        return sunset. sunrise and country
        """
        return self.response['sys']

    @property
    @try_except
    def main(self):
        """
        return main information of the weather
        """
        return self.response['main']

    @property
    @try_except
    def weather(self):
        """
        return more info Weather condition codes
        """
        return self.response['weather']

    @property
    @try_except
    def wind(self):
        """
        return wind speed, deg and gust
        """
        return self.response['wind']

    @property
    @try_except
    def rain(self):
        """
        return rain information
        """
        return self.response['rain']

    @property
    @try_except
    def snow(self):
        """
        return snow information
        """
        return self.response['snow']

    @property
    @try_except
    def clouds(self):
        """
        return Cloudiness, %
        """
        return self.response['clouds']

    @classmethod
    @try_except
    async def weather_text(cls, lat, lon, chat_id):
        if not (lat and lon):
            # taking coordinate (lat, lon) from database by chat_id
            coord = await db.select_lat_lon(chat_id)
            # unpacking tuple (lat, lon)
            lat, lon = coord['lat'], coord['lon']

        # Response from Weather API
        ####################################################
        if lat and lon:
            weather_response = cls(lat=lat, lon=lon)
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
                    f"This weather forecast is valid for the same time",
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
                    f"Wind Speed: {wind['speed']} m/s",
                    f"{f'Snow: {snow}' if snow else ''}",
                    f"{f'Rain: {rain}' if rain else ''}",
                    ]
            text_f = '\n'.join(text)

            return text_f
