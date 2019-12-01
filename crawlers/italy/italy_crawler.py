# -*- coding: utf-8 -*-

import json

import requests

from ..base import BaseCrawler


class ItalyCrawler(BaseCrawler):
    def get_events(self):
        response = requests.get(
            "https://raw.githubusercontent.com/ildoc/awesome-italy-events/master/data/2020.json"
        )

        for event in json.loads(response.content):
            if "pycon" in event["title"].lower():
                continue

            e = {
                "name": event["title"],
                "url": event["url"],
                "city": event["location"],
                "state": None,
                "country": "Italy",
                "cfp_open": False,
                "cfp_end_date": "1970-01-01",
                "start_date": event["startDate"],
                "end_date": event["endDate"],
                "source": "https://github.com/ildoc/awesome-italy-events",
                "tags": ["technology"],
                "kind": "conference",
                "by": "bot",
            }
            self.events.append(e)
