# -*- coding: utf-8 -*-

import datetime as dt

import json
import requests
from bs4 import BeautifulSoup as bs

from ..base import BaseCrawler

class WikicfpCrawler(BaseCrawler):
    def get_events(self):
        response = requests.get(
            "http://www.wikicfp.com/cfp/"
        )
        response.encoding = 'utf-8'
        soup = bs(response.content, 'html.parser')
        table = soup.find_all('div', class_='contsec')[2].form.table
        rows = table.find_all('tr')[5:]

        for i in range(0, len(rows), 2):
            
            top_row = rows[i].find_all('td')
            url = 'http://www.wikicfp.com' + top_row[0].a['href']
            name = top_row[1].text
            bottom_row = rows[i+1].find_all('td')
            date = bottom_row[0].text
            location = bottom_row[1].text

            city = state = country = None
            if ',' in location: 
                location_parsed = bottom_row[1].text.split(', ')
                print(location_parsed)
                // special cases
                if 'University' in location_parsed[0]:
                    city = location_parsed[1]
                elif len(location_parsed) == 3:
                    city, state, country = location_parsed
                elif len(location_parsed) == 2:
                    city, country = location_parsed
            
            if '-' in date:
                start_date, end_date = date.split(' - ') 
                print(start_date)
                print(end_date)

            s_cfp_end_date = bottom_row[2].text
            // special cases
            index = bottom_row[2].text.find('(')
            if index != -1:
                s_cfp_end_date = s_cfp_end_date[index+1: -1]
            
            cfp_end_date = dt.datetime.strptime(s_cfp_end_date, "%b %d, %Y")
            print(cfp_end_date)
            cfp_open = (
                True
                if dt.datetime.now() < cfp_end_date
                else False
            )

            source = "http://www.wikicfp.com/cfp/"
            tags = 'technology'
            kind = 'conference'
            by = 'N/A'
            
            e = {
                "name": name,
                "url": url,
                "city": city,
                "state": state,
                "country": country,
                "location": location,
                "cfp_open": cfp_open,
                "cfp_end_date": cfp_end_date,
                "start_date": start_date,
                "end_date": end_date,
                "source": source,
                "tags": tags,
                "kind": kind,
                "by": by,
            }

            self.events.append(e)
