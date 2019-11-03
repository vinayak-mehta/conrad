# -*- coding: utf-8 -*-

import os
import pickle
import datetime as dt
from html.parser import HTMLParser

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from ..base import BaseCrawler

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "href":
                self.url = attr[1]


class PyConCrawler(BaseCrawler):
    def get_events(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        service = build("calendar", "v3", credentials=creds)

        now = dt.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        cal_id_python_events = "j7gov1cmnqr9tvg14k621j7t5c@group.calendar.google.com"

        # Call the Calendar API
        print("Getting the upcoming events")
        events_result = (
            service.events()
            .list(
                calendarId=cal_id_python_events,
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
        else:
            for event in events:
                parser = MyHTMLParser()
                parser.feed(event["description"])

                url = "https://www.python.org/events/"
                if hasattr(parser, "url"):
                    url = parser.url

                city = state = country = None
                location = event["location"].split(",")
                if len(location) == 2:
                    city = location[0].strip()
                    country = location[1].strip()
                elif len(location) == 3:
                    city = location[0].strip()
                    state = location[1].strip()
                    country = location[2].strip()

                e = {
                    "name": event["summary"],
                    "url": url,
                    "city": city,
                    "state": state,
                    "country": country,
                    "cfp_open": False,
                    "cfp_start_date": "1970-01-01",
                    "cfp_end_date": "1970-01-01",
                    "start_date": event["start"]["date"],
                    "end_date": event["end"]["date"],
                    "source": "https://www.python.org/events/",
                    "tags": ["python"],
                    "kind": "conference",
                    "by": "bot",
                }
                self.events.append(e)
