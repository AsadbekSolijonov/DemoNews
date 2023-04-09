from pprint import pprint

from data import config
import requests
from api.api_decorator import try_except


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
