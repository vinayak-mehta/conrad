# -*- coding: utf-8 -*-

import os
import json
import datetime as dt

from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from ..base import BaseCrawler


class PythonCrawler(BaseCrawler):
    def get_events(self):
        credentials = Credentials.from_service_account_file(
            "google_service_account_credentials.json",
            scopes=[
                "https://www.googleapis.com/auth/calendar",
                "https://www.googleapis.com/auth/calendar.readonly",
            ],
        )
        service = build("calendar", "v3", credentials=credentials)

        start_time = dt.datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
        end_time = None
        events = []

        try:
            page_token = None
            while True:
                event_page = (
                    service.events()
                    .list(
                        singleEvents="False",
                        orderBy="startTime",
                        calendarId="j7gov1cmnqr9tvg14k621j7t5c@group.calendar.google.com",
                        pageToken=page_token,
                        timeMin=start_time,
                        timeMax=end_time,
                    )
                    .execute()
                )
                events.extend(list(event_page["items"]))

                page_token = event_page.get("nextPageToken")
                if not page_token:
                    break
        except AccessTokenRefreshError:
            print(
                "The credentials have been revoked or expired, please re-run"
                " the application to re-authorize."
            )

        for event in events:
            if any(
                [word in event["summary"].lower() for word in ["cancel", "postpone"]]
            ):
                continue

            try:
                soup = BeautifulSoup(event["description"], "html.parser")
                event_url = soup.find_all("a", href=True)[0]["href"]
            except IndexError:
                event_url = None

            if "date" in event["start"]:
                start_date = event["start"]["date"]
                end_date = event["end"]["date"]
            elif "dateTime" in event["start"]:
                start_date = event["start"]["dateTime"].split("T")[0]
                end_date = event["end"]["dateTime"].split("T")[0]
            else:
                raise ValueError("Event date not found!")

            e = {
                "name": event["summary"],
                "url": event_url,
                "city": None,
                "state": None,
                "country": None,
                "location": event.get("location"),
                "cfp_open": False,
                "cfp_end_date": "1970-01-01",
                "start_date": start_date,
                "end_date": end_date,
                "source": "https://wiki.python.org/moin/PythonEventsCalendar",
                "tags": ["python"],
                "kind": "conference",
                "by": "bot",
            }
            self.events.append(e)
