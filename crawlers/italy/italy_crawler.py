# -*- coding: utf-8 -*-

import json

import requests

from ..base import BaseCrawler


class ItalyCrawler(BaseCrawler):
    """
    Crawler for Italy events from the Awesome Italy Events dataset.

    Fetches conferences in Italy (except PyCon) and formats them
    according to Conrad's event schema.
    """
    def __init__(self, year = 2020):
        super().__init__()
        self.year = year
    
    def get_events(self):
        url = f"https://raw.githubusercontent.com/ildoc/awesome-italy-events/master/data/{self.year}.json"
        try:
            response = requests.get(url, timeout = 10)
            response.raise_for_status() # Raises an HTTP error for bad status codes
            data = json.loads(response.content.decode("utf-8-sig")) # Convert response to JSON
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch events for {self.year}: {e}")
            return
        except json.JSONDecodeError as e:
            print(f"Invalid JSON for {self.year}: {e}")
            return

        for event in data:
            if "pycon" in event.get("title", "").lower():
                continue

            # Skip if required fields are missing
            required_fields = ["title", "url", "location", "startDate", "endDate"]
            if not all(field in event for field in required_fields):
                continue
            
            e = {
                "name": event.get("title", "Untitled Event"),
                "url": event.get("url", ""),
                "city": event.get("location", None),
                "state": None,
                "country": "Italy",
                "location": event.get("location", ""),
                "cfp_open": False,
                "cfp_end_date": "1970-01-01",
                "start_date": event.get("startDate", "1970-01-01"),
                "end_date": event.get("endDate", "1970-01-01"),
                "source": "https://github.com/ildoc/awesome-italy-events",
                "tags": ["technology"],
                "kind": "conference",
                "by": "bot",
            }
            self.events.append(e)
