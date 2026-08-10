import requests
from bs4 import BeautifulSoup
import json
import datetime as dt

class DevEvent:
    def __init__(self, name, city, country, start_date, end_date, url):
        self.name = name
        self.url = url
        self.city = city
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.source = DevEventCrawler.URL
        self.tags = ["python", "developer", "conference"]
        self.kind = "conference"
        self.by = "bot"

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "city": self.city,
            "country": self.country,
            "start_date": self.start_date.strftime(DevEventCrawler.DATE_FORMAT),
            "end_date": self.end_date.strftime(DevEventCrawler.DATE_FORMAT),
            "source": self.source,
            "tags": self.tags,
            "kind": self.kind,
            "by": self.by,
        }


class DevEventCrawler:
    URL = "https://dev.events/python"
    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }
    DATE_FORMAT = "%Y-%m-%d"

    def _format_date(self, date_str):
        return dt.datetime.strptime(date_str.split('T')[0], self.DATE_FORMAT).date()

    def _parse_dev_event(self, event_json):
        try:
            name = event_json.get("name")
            start_date = self._format_date(event_json["startDate"])
            end_date = self._format_date(event_json["endDate"])
            city = event_json["location"]["address"]["addressLocality"]
            country = event_json["location"]["address"]["addressRegion"]
            url = event_json["url"]

            return DevEvent(
                name=name,
                city=city,
                country=country,
                start_date=start_date,
                end_date=end_date,
                url=url
            )
        except Exception as e:
            print(f"Failed to parse event: {e}")
            return None

    def _parse_dev_events(self, scripts):
        events = []
        for script in scripts:
            try:
                json_data = json.loads(script.string)
                if isinstance(json_data, dict) and json_data.get("@type") == "EducationEvent":
                    event = self._parse_dev_event(json_data)
                    if event:
                        events.append(event)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
        return events

    def get_events(self):
        resp = requests.get(self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(resp.content, 'html.parser')
        scripts = soup.find_all('script', type='application/ld+json')

        # Skip the first 3 scripts as they are promoted unrelated events
        scripts = scripts[3:]
        dev_events = self._parse_dev_events(scripts)
        self.events = [event.to_json() for event in dev_events if event]
        return self.events