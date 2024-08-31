import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    # Token File Che ke nai. User access che aema
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Badhu Complete? To Login Karo ne Mota..
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Credential Refresh Karo
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client-secret.json', SCOPES) 
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Google Drive service nu Builiding Point
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(file_path, file_name):
    """Upload a file to Google Drive."""
    service = authenticate()
    # File metadata.
    file_metadata = {
        'name': file_name,
        'mimeType': 'application/vnd.google-apps.document'  # Change mimeType if needed
    }
    # Upload file.
    media = MediaFileUpload(file_path, mimetype='text/plain')  # Adjust MIME type as needed
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

if __name__ == '__main__':
    file_path = 'key.txt'  # Replace with your file path
    file_name = 'uploaded_file_name.txt'  # Replace with the desired file name in Drive
    upload_file(file_path, file_name)
