# -*- coding: utf-8 -*-

from datetime import datetime

from bs4 import BeautifulSoup

import requests
import json


class PyDataCrawler:
    URL = 'https://pydata.org/event-schedule/'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
               'AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/50.0.2661.102 Safari/537.36'}
    SELECTOR = 'div.mec-event-list-classic > script[type="application/ld+json"]'
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self):
        self.events = []

    def get_events(self):
        resp = requests.get(self.URL, headers=self.HEADERS)
        page = BeautifulSoup(resp.content, features="html.parser")
        pydata_events = self.__parse_pydata_events(page.select(self.SELECTOR))
        self.events = [event.to_json() for event in pydata_events]
        return self.events

    def __format_date(self, date_str):
        return datetime.strptime(date_str, self.DATE_FORMAT).date()

    def __parse_pydata_event(self, event_article):
        content = json.loads(event_article.decode_contents())
        try:
            city, country = content['location']['name'].split(', ')
        except (KeyError, ValueError):
            city = None
            country = None
        return PyDataEvent(
                 name=content['name'],
                 country=country,
                 city=city,
                 start_date=self.__format_date(content['startDate']),
                 end_date=self.__format_date(content['endDate']),
                 url=content['url'])

    def __parse_pydata_events(self, event_articles):
        return list(map(self.__parse_pydata_event, event_articles))


class PyDataEvent:
    def __init__(self, name, country, city, start_date, end_date, url):
        self.name = name
        self.country = country
        self.city = city
        self.state = None
        self.kind = 'Event'
        self.source = PyDataCrawler.URL
        self.cfp_open = False
        self.cfp_end_date = None
        self.cfp_start_date = None
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.tags = ['python', 'pydata']
        self.by = 'bot'

    def to_json(self):
        return {'name': self.name,
                'country': self.country,
                'city': self.city,
                'state': self.state,
                'kind': self.kind,
                'source': self.source,
                'cfp_open': self.cfp_open,
                'cfp_end_date': self.cfp_end_date,
                'cfp_start_date': self.cfp_start_date,
                'start_date': self.start_date.strftime(
                    PyDataCrawler.DATE_FORMAT),
                'end_date': self.end_date.strftime(
                    PyDataCrawler.DATE_FORMAT),
                'url': self.url,
                'tags': self.tags,
                'by': self.by
                }
