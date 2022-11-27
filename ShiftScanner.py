from __future__ import print_function
from print_moonin import print_moonin
import datetime
import os.path
from datetime import timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys,time,random
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']





typing_speed = 70 #wpm
def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print('')

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    slow_type("Enter your surname: ")
    for line in sys.stdin:

        surname = line.strip()
        if 'Exit' == line.rstrip():
            break
        if line.rstrip():
            print(surname + ", you say, ok let's have a look")
            break


    creds = None
    when = ""

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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:


        service = build('calendar', 'v3', credentials=creds)



        def uploader(list):
            for i in list:
                print(i)
                i = i.isoformat()
                i = datetime.datetime.fromisoformat(i)

                event = {
                    'summary': f'{when} shift',
                    'description': f'Shift {when}',
                    'start': {
                        'dateTime': i.isoformat(),
                        'timeZone': 'Europe/Moscow'
                    },
                    'end': {
                        'dateTime': (i + timedelta(hours=12)).isoformat(),
                        'timeZone': 'Europe/Moscow',
                    },
                    'reminders':{
                        'useDefault' : False,
                        'overrides': [
                            {'method': 'popup', 'minutes': 1440},
                        ],
                        }

                }

                event = service.events().insert(calendarId='primary', body=event).execute()
                print('Event created: %s' % (event.get('htmlLink')))

        from getdates import get_shift_dates
        date = get_shift_dates(surname)

        up_date = date['Н']
        when = "Night"
        uploader(up_date)
        up_date = date['Д']
        when = "Day"
        uploader(up_date)
        up_date = date ['Д2']
        when = "Day 2"
        uploader(up_date)
        slow_type("Ok, now you won't miss a single shift, bro.")
        print_moonin()



    except HttpError as error:
        print('An error occurred: %s' % error)




if __name__ == '__main__':
        main()




