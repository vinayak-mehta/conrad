# -*- coding: utf-8 -*-

import datetime as dt

import json
import requests
from bs4 import BeautifulSoup

from ..base import BaseCrawler


class PyDataEvent:
    def __init__(self, name, country, city, start_date, end_date, url):
        self.name = name
        self.url = url
        self.city = city
        self.state = None
        self.country = country
        self.cfp_open = False
        self.cfp_end_date = "1970-01-01"
        self.start_date = start_date
        self.end_date = end_date
        self.source = PyDataCrawler.URL
        self.tags = ["python", "pydata"]
        self.kind = "conference"
        self.by = "bot"

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "cfp_open": self.cfp_open,
            "cfp_end_date": self.cfp_end_date,
            "start_date": self.start_date.strftime(PyDataCrawler.DATE_FORMAT),
            "end_date": self.end_date.strftime(PyDataCrawler.DATE_FORMAT),
            "source": self.source,
            "tags": self.tags,
            "kind": self.kind,
            "by": self.by,
        }


class PyDataCrawler(BaseCrawler):
    URL = "https://pydata.org/event-schedule/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/50.0.2661.102 Safari/537.36"
    }
    SELECTOR = 'div.mec-event-list-classic > script[type="application/ld+json"]'
    DATE_FORMAT = "%Y-%m-%d"

    def _format_date(self, date_str):
        return dt.datetime.strptime(date_str, self.DATE_FORMAT).date()

    def _parse_pydata_event(self, event_article):
        content = json.loads(event_article.decode_contents())

        try:
            city, country = content["location"]["name"].split(", ")
        except (KeyError, ValueError):
            city = None
            country = None

        return PyDataEvent(
            name=content["name"],
            url=content["url"],
            city=city,
            country=country,
            start_date=self._format_date(content["startDate"]),
            end_date=self._format_date(content["endDate"]),
        )

    def _parse_pydata_events(self, event_articles):
        return list(map(self._parse_pydata_event, event_articles))

    def get_events(self):
        resp = requests.get(self.URL, headers=self.HEADERS)
        page = BeautifulSoup(resp.content, features="html.parser")
        pydata_events = self._parse_pydata_events(page.select(self.SELECTOR))
        self.events = [event.to_json() for event in pydata_events]
