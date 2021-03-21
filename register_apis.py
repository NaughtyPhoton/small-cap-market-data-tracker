import json
import os

import os.path

import gspread
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

TD_JSON = f'{os.path.expanduser("~")}/sl_credentials/td.json'
GOOGLE_JSON = f'{os.path.expanduser("~")}/sl_credentials/sl_google_credentials.json'
GOOGLE_BOT_JSON = f'{os.path.expanduser("~")}/sl_credentials/slBot_google_credentials.json'
SPREADSHEET_ID = '1-FeM7uQWuybnnwwRgPVMNVTcaAh-jgEU4EMnqEcF0js'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_td_key() -> str:
    with open(TD_JSON) as f:
        return json.load(f)['consumer_key']


def get_sheets_service():
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
                GOOGLE_JSON, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    return service.spreadsheets()


def get_gspread_service():
    return gspread.service_account()


def get_gspread_sheet():
    return get_gspread_service().open_by_key(SPREADSHEET_ID)
