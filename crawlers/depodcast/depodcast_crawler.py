import re
import requests
from dateutil.parser import parse
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from ..base import BaseCrawler

class DEPodcastCrawler(BaseCrawler):

    def parse_date(self, event_dates):
        '''
        Function to parse date ranges and return the start and end dates
        '''
        if '-' in event_dates:
            start_dt = event_dates.split(' - ')[0]
            start_dt_formatted = datetime.strftime(parse(start_dt), '%Y-%m-%d')
            month = start_dt.split(' ')[0]
            end_dt = event_dates.split(' - ')[1] + ' ' +  month
            end_dt_formatted = datetime.strftime(parse(end_dt), '%Y-%m-%d')
        else:
            start_dt_formatted = datetime.strftime(parse(event_dates), '%Y-%m-%d')
            end_dt_formatted = datetime.strftime(parse(event_dates), '%Y-%m-%d')
        return (start_dt_formatted, end_dt_formatted)
    
    def requests_retry_session(self, retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
        session = requests.Session()
        retry = Retry(total=retries,
                      read=retries,
                      connect=retries,
                      backoff_factor=backoff_factor,
                      status_forcelist=status_forcelist
                     )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_events(self):
        geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
        URL = 'https://www.dataengineeringpodcast.com/conferences/'
        response = self.requests_retry_session().get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find(id='post-1401')
        conf_list = results.find_all("section", class_='elementor-element')
        for conf in conf_list:
            title = conf.find('h2', class_='elementor-heading-title elementor-size-default')
            place = conf.find('div', class_='elementor-custom-embed')
            city = 'Online'
            state = ''
            country = 'Online'
            if title is not None and "Subscribe" not in title.text:
                if place is not None:
                    event_info = title.text
                    hyp_index = event_info.index(' - ')
                    event_name_and_loc = event_info[:hyp_index]
                    event_dates = event_info[hyp_index+3:]
                    start_dt_formatted, end_dt_formatted = self.parse_date(event_dates)
                    event_link = conf.find('a')['href']
                    place = place.iframe.extract().attrs['aria-label']
                    if "Convention Center" in place:
                        pattern = re.compile(r'[a-zA-z\.\- ]*Convention Center')
                        match = pattern.finditer(place)
                        for m in match:
                            place = m.group()
                    complete_addr = geolocator.geocode(place).address
                    city = complete_addr.split(',')[-5].strip()
                    state = complete_addr.split(',')[-3].strip()
                    country = complete_addr.split(',')[-1].strip()
                else:
                    event_info = title.text
                    hyp_index = event_info.index(' - ')
                    event_name_and_loc = event_info[:hyp_index]
                    event_dates = event_info[hyp_index+3:]
                    start_dt_formatted, end_dt_formatted = self.parse_date(event_dates)
                    event_link = conf.find('a')['href']
                
                e = {
                    "name": event_name_and_loc,
                    "url": event_link,
                    "city": city,
                    "state": state,
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
                print(e)
                self.events.append(e)
