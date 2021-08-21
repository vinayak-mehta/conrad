# -*- coding: utf-8 -*-

from ..base import BaseCrawler
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class SorseCrawler(BaseCrawler):
    def get_events(self):
        # Populate this list of events using your code
        events = []

        # YOUR CODE HERE

        URL = "https://sorse.github.io/programme/"

        res = requests.get(URL)
        soup = BeautifulSoup(res.text,"html.parser")
        
        for event in soup.find_all("div",class_="card col-12 post-card"):
            data =  {
                    "name": None,
                    "url": "https://sorse.github.io/programme/",
                    "city": None,
                    "state": None,
                    "country": None,
                    "cfp_open": False,
                    "cfp_end_date": "1970-01-01",
                    "start_date": None,
                    "end_date": None,
                    "source": "https://sorse.github.io/programme",
                    "tags": None,
                    "kind": "conference",
                    "by": "bot",
                }
            temp = event.select("a[href]")
            data["name"] = temp[0].get_text()
            data["url"] += temp[0].get('href')
            temp2 = event.select("time[datetime]")
            try:
                data["start_date"] = date_for(temp2[0].get_text().strip()[:-7])
            except IndexError:
                data["start_date"] = None
            try:
                data["end_date"] = date_for(temp2[0].get_text().strip()[:-7])
            except IndexError:
                data["end_date"] = None
            self.events.append(data)

    def date_for(s):
        d = datetime.strptime(s,'%B %d, %Y')
        return d.strftime('%d/%m/%Y')