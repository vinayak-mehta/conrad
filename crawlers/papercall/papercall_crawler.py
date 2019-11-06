# -*- coding: utf-8 -*-
# https://github.com/coderanger/cfp-scraper/blob/master/papercall.py

import requests
import dateparser
import dateparser.search
from bs4 import BeautifulSoup

from ..base import BaseCrawler


URL = "https://www.papercall.io/events?open-cfps=true&page={page}"


def get(page):
    res = requests.get(URL.format(page=page))
    return BeautifulSoup(res.text, "html.parser")


def maybe_int(s):
    try:
        return int(s)
    except ValueError:
        return 0


def num_pages():
    pagination = get(1).find(class_="pagination")
    return max(maybe_int(elm.string) for elm in pagination.find_all("a"))


def parse_page(root):
    for event in root.select(".event-list-detail"):
        title_line = event.select(".event__title a")[-1]
        title_parts = title_line.string.split(" - ", 1)
        if len(title_parts) == 1:
            title = title_parts[0]
            location = ""
        elif len(title_parts) == 2:
            title = title_parts[0]
            location = title_parts[1]
        try:
            url = event.select(".fa-external-link")[0]["title"]
        except IndexError:
            url = ""
        cfp_close_label = event.find(
            lambda elm: elm.name == "strong" and "CFP closes at" in elm.string
        )
        if not cfp_close_label:
            # No real point.
            continue
        cfp_close = dateparser.parse(
            cfp_close_label.parent.find_next_sibling("td").string.strip()
        )
        start_date = end_date = None
        dates = event.find(
            lambda elm: elm.name == "strong" and "Event Dates" in elm.string
        )
        if dates:
            dates = dates.next_sibling.string.strip()
        if dates:
            parsed_dates = [d for _, d in dateparser.search.search_dates(dates)]
            if parsed_dates:
                start_date = parsed_dates[0].date()
                end_date = parsed_dates[-1].date()
        tags = [t.string for t in event.select('a[href^="/events?keywords=tags"]')]

        today = dateparser.parse("now UTC")
        cfp_open = False if today > cfp_close else True
        try:
            city = location.split(",")[0]
            country = location.split(",")[1]
        except IndexError:
            city = country = location

        yield {
            "name": title,
            "url": url,
            "city": city,
            "state": None,
            "country": country,
            "cfp_open": cfp_open,
            "cfp_end_date": cfp_close.strftime("%Y-%m-%d")
            if cfp_close is not None
            else "1970-01-01",
            "start_date": start_date.strftime("%Y-%m-%d")
            if start_date is not None
            else "1970-01-01",
            "end_date": end_date.strftime("%Y-%m-%d") if end_date is not None else None,
            "source": "http://papercall.io",
            "tags": tags,
            "kind": "conference",
            "by": "bot",
        }


def parse_all():
    count = num_pages()
    for n in range(count):
        yield from parse_page(get(n + 1))


class PapercallCrawler(BaseCrawler):
    def get_events(self):
        for event in parse_all():
            self.events.append(event)
