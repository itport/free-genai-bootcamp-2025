import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_google_drive_service():
    """
    Get or create Google Drive API service
    """
    creds = None
    
    # Load saved credentials if they exist
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials are invalid or don't exist, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path):
    """
    Upload a file to Google Drive and return its shareable link
    
    Args:
        file_path (str): Path to the file to upload
        
    Returns:
        str: Shareable link to the uploaded file
    """
    try:
        service = get_google_drive_service()
        file_metadata = {'name': Path(file_path).name}
        
        media = MediaFileUpload(
            file_path,
            mimetype='audio/mpeg',
            resumable=True
        )
        
        # Upload file
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        # Make the file accessible via link
        service.permissions().create(
            fileId=file.get('id'),
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()
        
        # Get the shareable link
        return f"https://drive.google.com/file/d/{file.get('id')}/view"
        
    except Exception as e:
        print(f"Error uploading to Google Drive: {str(e)}")
        return None

def test_drive_upload():
    """
    Test function to validate Google Drive upload functionality
    """
    # Load environment variables
    load_dotenv()
    
    # Test directory containing MP3 files
    videos_dir = Path(os.path.abspath('./videos'))
    
    if not videos_dir.exists():
        print(f"Error: Videos directory not found at {videos_dir}")
        return
    
    # Test with each MP3 file in the videos directory
    mp3_files = list(videos_dir.glob("*.mp3"))
    
    if not mp3_files:
        print("No MP3 files found in the videos directory")
        return
    
    print(f"Found {len(mp3_files)} MP3 files to test")
    
    for mp3_file in mp3_files:
        print(f"\nTesting upload for: {mp3_file.name}")
        share_link = upload_to_drive(str(mp3_file))
        
        if share_link:
            print(f"Successfully uploaded {mp3_file.name}")
            print(f"Shareable link: {share_link}")
        else:
            print(f"Failed to upload {mp3_file.name}")

if __name__ == "__main__":
    test_drive_upload()