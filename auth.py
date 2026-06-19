import os
import json
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]


def get_google_services():
    creds = None

    # Try Streamlit Cloud secrets first
    try:
        token_data = json.loads(st.secrets["GOOGLE_TOKEN_JSON"])
        creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    except Exception:
        # Fall back to local token.json
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        if not hasattr(st, 'secrets') or "GOOGLE_TOKEN_JSON" not in st.secrets:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    gmail_service = build('gmail', 'v1', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)

    print("✅ Gmail and Calendar connected successfully!")
    return gmail_service, calendar_service


if __name__ == "__main__":
    gmail, calendar = get_google_services()