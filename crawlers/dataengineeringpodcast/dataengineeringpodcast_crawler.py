import requests
from dateutil.parser import parse
from datetime import datetime
from bs4 import BeautifulSoup
from ..base import BaseCrawler

class DataEngineeringPodcastCrawler(BaseCrawler):
    def get_events(self):
        events = []
        self.events.append(events)

""" def parse_info(self, event_info):
    # Get index of 1st '-'. All event info follow the pattern: {Event Name} {Location} - {Month} {Start Date} - {End Date}
    hyp_index = event_info.index(' - ')
    event_name_and_loc = event_info[:hyp_index]
    event_dates = event_info[hyp_index+3:]
    return (event_name_and_loc, event_dates) """

def get():
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
            print(event_name_and_loc)
            start_dt = event_dates.split(' - ')[0]
            start_dt_formatted = datetime.strftime(parse(start_dt), '%Y-%m-%d')
            month = start_dt.split(' ')[0]
            end_dt = event_dates.split(' - ')[1] + ' ' +  month
            end_dt_formatted = datetime.strftime(parse(end_dt), '%Y-%m-%d')
            print(start_dt_formatted, '=========', end_dt_formatted)
            event_link = conf.find('a')['href']
            print(event_link)
            city = place.iframe.extract().attrs['aria-label']
            print(city)

get()
