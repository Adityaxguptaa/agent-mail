from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64, os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SEEN_SNIPPET = None  # Global to track latest email

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

def check_latest_email(service):
    global SEEN_SNIPPET
    result = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=1).execute()
    messages = result.get('messages', [])
    if not messages:
        return None

    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    snippet = msg.get('snippet')

    if snippet != SEEN_SNIPPET:
        SEEN_SNIPPET = snippet
        return snippet
    return None
