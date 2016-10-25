from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, tzinfo,timedelta
from rfc3339 import rfc3339

import datetime
import argparse


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def convert_to_rfc3339(date):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])

    min_time = datetime.datetime(year, month, day, 0, 0, 0)
    max_time = datetime.datetime(year, month, day, 23, 59, 59)
    #print(max_time)
    min_time_rfc = rfc3339(min_time, utc=True, use_system_timezone=False)[:-1]+'+08:00'
    max_time_rfc = rfc3339(max_time, utc=True, use_system_timezone=False)[:-1]+'+08:00'
    return min_time_rfc, max_time_rfc


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_events(date):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    min_time, max_time = convert_to_rfc3339(date)
    #print(now)
    #print(max_time, min_time)

    eventsResult = service.events().list(
        calendarId='primary', timeMax=max_time, singleEvents=True, timeMin= min_time,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No  events found.')
    else:
        print('get %d events.' % len(events))
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('date', help='date to get events')
    args = parser.parse_args()
    get_events(args.date)


if __name__ == '__main__':
    main()
