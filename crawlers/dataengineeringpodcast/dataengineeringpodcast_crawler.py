import re
import requests
from dateutil.parser import parse
from datetime import datetime
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from ..base import BaseCrawler

class DataEngineeringPodcastCrawler(BaseCrawler):

    def get_events(self):
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
        URL = 'https://www.dataengineeringpodcast.com/conferences/'
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find(id='post-1401')
        conf_list = results.find_all("section", class_='elementor-element')
        for conf in conf_list:
            title = conf.find('h2', class_='elementor-heading-title elementor-size-default')
            place = conf.find('div', class_='elementor-custom-embed')
            if title is not None and "Subscribe" not in title.text and place is not None:
                event_info = title.text
                hyp_index = event_info.index(' - ')
                event_name_and_loc = event_info[:hyp_index]
                event_dates = event_info[hyp_index+3:]
                start_dt = event_dates.split(' - ')[0]
                start_dt_formatted = datetime.strftime(parse(start_dt), '%Y-%m-%d')
                month = start_dt.split(' ')[0]
                end_dt = event_dates.split(' - ')[1] + ' ' +  month
                end_dt_formatted = datetime.strftime(parse(end_dt), '%Y-%m-%d')
                event_link = conf.find('a')['href']
                place = place.iframe.extract().attrs['aria-label']
                if "Convention Center" in place:
                    pattern = re.compile(r'[a-zA-z\.\- ]*Convention Center')
                    match = pattern.finditer(place)
                    for m in match:
                        place = m.group()
                complete_addr = geolocator.geocode(place).address
                last_comma = complete_addr.rfind(',')
                country = complete_addr[(last_comma+1):].strip()

                e = {
                    "name": event_name_and_loc,
                    "url": event_link,
                    "city": place,
                    "state": None,
                    "country": country,
                    "cfp_open": False,
                    "cfp_end_date": "1970-01-01",
                    "start_date": start_dt_formatted,
                    "end_date": end_dt_formatted,
                    "source": "https://www.dataengineeringpodcast.com/conferences/",
                    "tags": ["data engineering"],
                    "kind": "conference",
                    "by": "bot",
                }

                self.events.append(e)
