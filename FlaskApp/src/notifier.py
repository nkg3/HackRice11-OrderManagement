from __future__ import print_function

import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def addEvent(summary: str, location: str, description: str, start_time: datetime, end_time: datetime):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S-05:00"),
            'timeZone': "America/Los_Angeles"
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S-05:00"),
            'timeZone': "America/Los_Angeles"
        }
    }

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './DataFiles/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    service.events().insert(calendarId='primary', body=event).execute()

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()

class Notifier:

    def __init__(self) -> None:
        load_dotenv()
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(account_sid, auth_token)


    def notify_new_order(self, worker_name: str, phone_number: str, facility_id: str, equipment_id: str,
                         start_time: datetime, end_time: datetime) -> str:
        body_str = 'New work order assigned to ' + worker_name + '. Report to ' + equipment_id + ' at ' + facility_id + '. Submit task at https://localhost:5000/worker/'+worker_name 
        message = self.client.messages.create(
                                body=body_str,
                                from_='+17133641490',
                                to=phone_number
                                )
        summary: str = "Work order at " + facility_id + " on " + start_time.strftime("%m/%d at %H:%M")
        addEvent(summary, facility_id, "", start_time, end_time)

        return(message.sid)