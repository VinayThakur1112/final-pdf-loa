import os
import base64
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from src.config import Config

logger = logging.getLogger(__name__)

class EmailClient:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticates with Gmail API."""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', Config.GMAIL_SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    logger.warning(f"Failed to refresh token: {e}")
                    self.creds = None
            
            if not self.creds and os.path.exists(Config.GOOGLE_CREDENTIALS_PATH):
                 # This flow is for local interactive runs; in server environments, use Service Account or mounted tokens
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        Config.GOOGLE_CREDENTIALS_PATH, Config.GMAIL_SCOPES)
                    self.creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open('token.json', 'w') as token:
                        token.write(self.creds.to_json())
                except Exception as e:
                    logger.error(f"Failed to authenticate with client secrets: {e}")
            
        if self.creds:
            self.service = build('gmail', 'v1', credentials=self.creds)
            logger.info("Gmail API service built successfully.")
        else:
            logger.warning("Could not authenticate. Email features will not work.")

    def fetch_emails(self, query="is:unread has:attachment"):
        """Fetches emails matching the query."""
        if not self.service:
            logger.error("Gmail service not initialized.")
            return []

        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            logger.info(f"Found {len(messages)} emails.")
            return messages
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []

    def get_email_details(self, msg_id):
        """Retrieves full email details including payload."""
        if not self.service:
            return None
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id).execute()
            return message
        except Exception as e:
            logger.error(f"Error getting email details for {msg_id}: {e}")
            return None

    def download_attachments(self, msg_id, store_dir="/tmp"):
        """Downloads PDF attachments from a message."""
        message = self.get_email_details(msg_id)
        if not message:
            return []

        downloaded_files = []
        parts = message.get('payload', {}).get('parts', [])
        
        # Sometimes parts are nested
        if not parts and 'body' in message.get('payload', {}):
             # Simple message without multipart? Unlikely for attachments.
             pass

        for part in parts:
            if part.get('filename') and part.get('filename').lower().endswith('.pdf'):
                if 'data' in part['body']:
                    data = part['body']['data']
                elif 'attachmentId' in part['body']:
                    att_id = part['body']['attachmentId']
                    att = self.service.users().messages().attachments().get(
                        userId='me', messageId=msg_id, id=att_id).execute()
                    data = att['data']
                else:
                    continue
                
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                path = os.path.join(store_dir, part['filename'])
                
                with open(path, 'wb') as f:
                    f.write(file_data)
                
                downloaded_files.append(path)
                logger.info(f"Downloaded attachment: {path}")

        return downloaded_files
