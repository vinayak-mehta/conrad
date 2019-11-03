# -*- coding: utf-8 -*-

import os
import datetime as dt

import pandas

from ..base import BaseCrawler


class PyConCrawler(BaseCrawler):
    def get_events(self):
        df = pandas.read_csv(
            "https://raw.githubusercontent.com/python-organizers/conferences/master/2020.csv"
        )

        for event in df.to_dict(orient="records"):
            location = event["Location"].split(",")
            city = state = country = None
            if len(location) == 2:
                city = location[0].strip()
                country = location[1].strip()
            elif len(location) == 3:
                city = location[0].strip()
                state = location[1].strip()
                country = event["Country"]

            e = {
                "name": event["Subject"],
                "url": event["Website URL"],
                "city": city,
                "state": state,
                "country": country,
                "cfp_open": False,
                "cfp_start_date": "1970-01-01",
                "cfp_end_date": "1970-01-01",
                "start_date": event["Start Date"],
                "end_date": event["End Date"],
                "source": "https://github.com/python-organizers/conferences",
                "tags": ["python"],
                "kind": "conference",
                "by": "bot",
            }
            self.events.append(e)
