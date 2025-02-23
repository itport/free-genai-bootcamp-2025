import os
from pathlib import Path
import requests
from dotenv import load_dotenv

def upload_to_salad_storage(audio_file_path, salad_api_key, organization_name, mime_type="audio/mpeg"):
    """
    Uploads an audio file to Salad Storage and generates a signed access URL.

    Args:
        audio_file_path (str): Path to the audio file.
        salad_api_key (str): Salad API key for authentication.
        organization_name (str): Name of the Salad organization.
        mime_type (str): MIME type of the file (default: "audio/mpeg").

    Returns:
        str: The signed URL for the uploaded file.
    """
    try:
        # Generate the upload URL
        file_name = f"audio/{Path(audio_file_path).name}"
        upload_url = f"https://storage-api.salad.com/organizations/{organization_name}/files/{file_name}"

        # Prepare headers for authentication
        headers = {
            "Salad-Api-Key": salad_api_key
        }

        # Prepare data for the upload
        data = {
            "mimeType": mime_type,
            "sign": "true",
            "signatureExp": str(3 * 24 * 60 * 60)  # 3 days in seconds
        }

        # Prepare the file to be uploaded
        with open(audio_file_path, "rb") as f:
            files = {"file": (Path(audio_file_path).name, f, mime_type)}
            response = requests.put(upload_url, headers=headers, data=data, files=files)
            response.raise_for_status()

        # Extract and return the signed URL
        result = response.json()
        signed_url = result.get("url")
        if not signed_url:
            raise ValueError("Signed URL not returned by the API.")
        return signed_url

    except requests.exceptions.RequestException as e:
        print(f"Error uploading to Salad storage: {e}")
    except ValueError as ve:
        print(f"API response error: {ve}")
    return None

def test_salad_upload():
    """
    Test function to validate the Salad storage upload functionality.
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
        signed_url = upload_to_salad_storage(
            str(mp3_file),
            salad_api_key,
            organization_name
        )
        
        if signed_url:
            print(f"Successfully uploaded {mp3_file.name}")
            print(f"Signed URL: {signed_url}")
        else:
            print(f"Failed to upload {mp3_file.name}")

if __name__ == "__main__":
    test_salad_upload()