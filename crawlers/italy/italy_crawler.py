# -*- coding: utf-8 -*-

import json

import requests

from ..base import BaseCrawler
from datetime import datetime


class ItalyCrawler(BaseCrawler):

    def get_events(self):
        current_year = datetime.now().year        
        use_year = current_year

        while self.get_data_for_year(use_year):
            use_year += 1

    def get_data_for_year (self, year):

        response = requests.get(
            "https://raw.githubusercontent.com/ildoc/awesome-italy-events/master/data/" + str(year) + ".json"
        )
        
        if response.status_code != 200:
            return False
        
        current_date = datetime.date(datetime.now())
        for event in json.loads(response.content):

            if "pycon" in event["title"].lower():
                continue
            
            conference_date = datetime.strptime(event["endDate"], '%Y-%m-%d').date()
            if conference_date >= current_date:
                e = {
                    "name": event["title"],
                    "url": event["url"],
                    "city": event["location"],
                    "state": None,
                    "country": "Italy",
                    "location": event["location"],
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
        return True
        

