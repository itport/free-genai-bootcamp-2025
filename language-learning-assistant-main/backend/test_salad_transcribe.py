import os
import requests
from dotenv import load_dotenv
from test_azure_blob import test_azure_blob_access

# Load environment variables
load_dotenv()

# API Configuration
SALAD_API_KEY = os.getenv("SALAD_API_KEY", "").strip()
SALAD_ORGANIZATION_NAME = os.getenv("SALAD_ORGANIZATION_NAME", "").strip()

def request_transcription(url, organization_name=None, api_key=None):
    """
    Request a transcription job from Salad API using an Azure blob URL.
    
    Args:
        url (str): Azure blob URL containing the audio/video file
        organization_name (str): Salad organization name (optional)
        api_key (str): Salad API key (optional)
        
    Returns:
        dict: API response containing job information
    """
    try:
        # Validate Azure blob URL access first
        if not test_azure_blob_access(url):
            raise ValueError("Azure blob URL is not accessible")
            
        # Get credentials from environment variables if not provided
        organization_name = organization_name or SALAD_ORGANIZATION_NAME
        api_key = api_key or SALAD_API_KEY
        
        if not organization_name or not api_key:
            raise ValueError("Missing required credentials. Set SALAD_ORGANIZATION_NAME and SALAD_API_KEY environment variables")
            
        # Clean and validate organization name
        organization_name = organization_name.strip()
        if not all(c.isalnum() or c == '-' for c in organization_name):
            raise ValueError("Organization name contains invalid characters. Use only alphanumeric characters and hyphens.")
            
        # Prepare API request
        endpoint = f"https://api.salad.com/api/public/organizations/{organization_name}/inference-endpoints/transcribe/jobs"
        
        headers = {
            "Salad-Api-Key": api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "input": {
                "url": url,
                "return_as_file": True,
                "language_code": "en",
                "sentence_level_timestamps": False,
                "word_level_timestamps": False,
                "diarization": False,
                "sentence_diarization": False,
                "srt": True
            },
            "metadata": {
                "source": "azure-blob"
            }
        }
        
        # Send transcription request
        print("\nSubmitting transcription request...")
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        print("\n✓ Transcription job submitted successfully!")
        print(f"Job ID: {result.get('id')}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ API request failed: {str(e)}")
        return None
    except ValueError as ve:
        print(f"\n✗ Validation error: {str(ve)}")
        return None
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    # Use the test URL from Azure blob testing
    test_url = "https://satranscription.blob.core.windows.net/transcription-unit-tests/That%20Little%20Voice.mp4?sp=r&st=2024-08-06T21:52:25Z&se=2027-04-01T05:52:25Z&spr=https&sv=2022-11-02&sr=b&sig=BMH0oUSmMlzne5%2BuFK0L6z2P6So8OOubieAk%2BVIpIiE%3D"
    
    print("Salad API Transcription Test")
    print("-" * 30)
    
    result = request_transcription(test_url)
    
    if result:
        print("\nFull API Response:")
        print("-" * 20)
        for key, value in result.items():
            print(f"{key}: {value}")