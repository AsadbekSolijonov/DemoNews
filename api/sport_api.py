import time
from pprint import pprint

from data import config
import requests
from api.api_decorator import try_except


class SportApiNews:
    """
    Docs: https://newsapi.org/
    """

    def __init__(self):
        self.api_key = config.SPORT_API_KEY
        self._country = 'us'
        self._category = 'sports'
        self.url = 'https://newsapi.org/v2/top-headlines?country={1}&category={2}&apiKey={0}'

    @property
    def request(self):
        url = self.url.format(self.api_key, self._country, self._category)
        result = requests.get(url=url).json()
        return result

    @property
    def response(self):
        result = self.request
        return result

    @property
    def status(self):
        result = self.response['status']
        return result

    @property
    @try_except
    def total_results(self):
        result = self.response['totalResults']
        return result

    @property
    @try_except
    def articles(self):
        result = self.response['articles']
        return result

    @property
    @try_except
    def yield_text(self):
        if self.status == 'ok':
            for article in self.articles:
                text = (f"Author: {article['author']}",
                        f"Content: {article['content']}",
                        f"Description: {article['description']}",
                        f"Published_at: {article['publishedAt']}",
                        f"Tag: #{article['source']['name']}"
                        f"Title: {article['title']}",
                        )
                text = '\n'.join(text)
                yield text


# x = SportApiNews()
# y = x.response
# z = x.total_results
# pprint(y, indent=2)
# print(z)