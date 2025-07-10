import calendar
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES= ['https://www.googleapis.com/auth/calendar'] # scope for full access
def main():
    creds = None
    # the file token.json stores the user's access token and refresh token, and is created automaticallywhen the authorization flow completes for the first time 
    # checking for token.json
    if os.path.exists('.secrets/token.json'):
        creds = Credentials.from_authorized_user_file(".secrets/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: 
            flow = InstalledAppFlow.from_client_secrets_file(".secrets/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # save credentials for the next run 
        with open('.secrets/token.json', 'w') as token:
            token.write(creds.to_json())
    try: 
        service = build('calendar', 'v3', credentials=creds)
        # calling API 
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print("Getting the upcoming 10 events")
        events_result = (
            service.events().list(
                calendarId = 'primary',
                timeMin = now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime',
            ).execute()
        )
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events')
            return
        
        # print START and name of th next 10 upcoming events
        for event in events:
            start = event['start'].get('dateTime'), event['start'].get('date')
            print(start, event['summary'])
        
    except HttpError as error :
        print(f'An error occured: {error}')
        
if __name__ == '__main__':
    main()