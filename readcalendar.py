import os, sys
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, tzinfo,timedelta
import dateutil.parser
import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Bot Client'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def time_range(datestr):
    date = dateutil.parser.parse(datestr)

    min_time = datetime.datetime(date.year, date.month, date.day, 0, 0, 0) + datetime.timedelta(hours=8)
    max_time = datetime.datetime(date.year, date.month, date.day, 23, 59, 59) + datetime.timedelta(hours=8)

    return min_time, max_time

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
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    print('-'* 50)
    return credentials

def get_events(min_time, max_time):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    print service.calendarList().list().execute()
    print(service.calendarList)

    eventsResult = service.events().list(
        calendarId='primary', timeMax=max_time.isoformat() + 'Z', singleEvents=True,
        timeMin=min_time.isoformat() + 'Z',
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No events found.')
    else:
        print('get %d events.' % len(events))
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


def main():

    date = '20161025'
    min_time, max_time = time_range(date)
    print(min_time, max_time)
    #get_events(min_time, max_time)

if __name__ == '__main__':
    main()