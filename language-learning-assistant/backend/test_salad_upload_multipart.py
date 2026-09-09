import os
from pathlib import Path
import requests
from dotenv import load_dotenv

def test_salad_upload_multipart():
    """
    Test function to validate the Salad storage upload functionality using multipart form data.
    """
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment variables
    salad_api_key = os.getenv("SALAD_API_KEY")
    organization_name = os.getenv("SALAD_ORGANIZATION_NAME")
    
    if not salad_api_key or not organization_name:
        print("Error: Missing required environment variables SALAD_API_KEY or SALAD_ORGANIZATION_NAME")
        return
    
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
        
        # Generate the upload URL
        file_name = f"audio/{mp3_file.name}"
        url = f"https://storage-api.salad.com/organizations/{organization_name}/files/{file_name}"
        
        # Prepare the multipart form data
        with open(mp3_file, 'rb') as f:
            files = {
                'file': (mp3_file.name, f, 'audio/mpeg')
            }
            
            data = {
                'mimeType': 'audio/mpeg',
                'sign': 'true',
                'signatureExp': str(3 * 24 * 60 * 60)  # 3 days in seconds
            }
            
            headers = {
                'Salad-Api-Key': salad_api_key
            }
            
            try:
                response = requests.put(url, files=files, data=data, headers=headers)
                response.raise_for_status()
                
                # Extract and print the signed URL
                result = response.json()
                if 'url' in result:
                    print(f"Successfully uploaded {mp3_file.name}")
                    print(f"Signed URL: {result['url']}")
                else:
                    print(f"Failed to get signed URL for {mp3_file.name}")
                    print(f"Response: {response.text}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Error uploading {mp3_file.name}: {e}")
                if hasattr(e.response, 'text'):
                    print(f"Response: {e.response.text}")

if __name__ == "__main__":
    test_salad_upload_multipart()