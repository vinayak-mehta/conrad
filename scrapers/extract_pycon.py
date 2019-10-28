from __future__ import print_function

import os.path
import pickle
import datetime

import simplejson as json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")

    cal_id_python_events = os.environ['calendar_id']
    cal_id_user_group = os.environ['group_id']

    items = []

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
    items.extend(events)

    # events_result = (
    #     service.events()
    #     .list(
    #         calendarId=cal_id_user_group,
    #         timeMin=now,
    #         singleEvents=True,
    #         orderBy="startTime",
    #     )
    #     .execute()
    # )
    # events = events_result.get("items", [])
    # items.extend(events)

    if not items:
        print("No upcoming events found.")

    data = {"items": items}
    json.dump(data, open('pycon.json', 'w'))

if __name__ == "__main__":
    
    if os.environ.get('calendar_id') == None:
        print("Something went wrong. You may not have exported correctly the environment variable \'calendar_id\'")
    elif os.environ.get('group_id') == None:
        print("Something went wrong. You may not have exported correctly the environment variable \'group_id\'")
    else:
        main()
