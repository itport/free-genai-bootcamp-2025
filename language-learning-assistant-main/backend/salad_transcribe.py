import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
SALAD_API_KEY = os.getenv("SALAD_API_KEY", "").strip()
SALAD_ORGANIZATION_NAME = os.getenv("SALAD_ORGANIZATION_NAME", "").strip()

def request_transcription(url, organization_name=None, api_key=None, **kwargs):
    """
    Request a transcription job from Salad API using a URL.
    
    Args:
        url (str): URL containing the audio/video file
        organization_name (str): Salad organization name (optional)
        api_key (str): Salad API key (optional)
        **kwargs: Additional parameters for the transcription job
            - return_as_file (bool): Whether to return the transcription as a file
            - language_code (str): Language code for transcription
            - translate (str): Translation option (e.g., "to_eng")
            - sentence_level_timestamps (bool): Include sentence-level timestamps
            - word_level_timestamps (bool): Include word-level timestamps
            - diarization (bool): Enable speaker diarization
            - sentence_diarization (bool): Enable sentence-level diarization
            - srt (bool): Generate SRT format
            - summarize (int): Number of words for summary
            - llm_translation (str): Languages for LLM translation (comma-separated)
            - srt_translation (str): Languages for SRT translation (comma-separated)
            - custom_vocabulary (str): Custom vocabulary terms (comma-separated)
            - webhook (str): Webhook URL for job completion notification
            - metadata (dict): Custom metadata for the job
        
    Returns:
        dict: API response containing job information
    """
    try:
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
        
        # Default input parameters
        input_params = {
            "url": url,
            "return_as_file": kwargs.get("return_as_file", True),
            "language_code": kwargs.get("language_code", "en"),
        }
        
        # Add optional parameters if they exist in kwargs
        optional_params = [
            "translate", "sentence_level_timestamps", "word_level_timestamps",
            "diarization", "sentence_diarization", "srt", "summarize",
            "llm_translation", "srt_translation", "custom_vocabulary"
        ]
        
        for param in optional_params:
            if param in kwargs and kwargs[param]:
                input_params[param] = kwargs[param]
        
        # Prepare the request data
        data = {
            "input": input_params,
            "metadata": kwargs.get("metadata", {"source": "salad-storage"})
        }
        
        # Add webhook if provided
        if "webhook" in kwargs and kwargs["webhook"]:
            data["webhook"] = kwargs["webhook"]
        
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
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return {"error": str(e)}
    except ValueError as ve:
        print(f"\n✗ Validation error: {str(ve)}")
        return {"error": str(ve)}
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        return {"error": str(e)}

def check_job_status(job_id, organization_name=None, api_key=None):
    """
    Check the status of a transcription job.
    
    Args:
        job_id (str): The ID of the job to check
        organization_name (str): Salad organization name (optional)
        api_key (str): Salad API key (optional)
        
    Returns:
        dict: API response containing job status information
    """
    try:
        # Get credentials from environment variables if not provided
        organization_name = organization_name or SALAD_ORGANIZATION_NAME
        api_key = api_key or SALAD_API_KEY
        
        if not organization_name or not api_key:
            raise ValueError("Missing required credentials. Set SALAD_ORGANIZATION_NAME and SALAD_API_KEY environment variables")
            
        # Clean and validate organization name
        organization_name = organization_name.strip()
        
        # Prepare API request
        endpoint = f"https://api.salad.com/api/public/organizations/{organization_name}/inference-endpoints/transcribe/jobs/{job_id}"
        
        headers = {
            "Salad-Api-Key": api_key
        }
        
        # Send status request
        print(f"\nChecking status for job {job_id}...")
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✓ Job status: {result.get('status')}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ API request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return {"error": str(e)}
    except ValueError as ve:
        print(f"\n✗ Validation error: {str(ve)}")
        return {"error": str(ve)}
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test with a sample URL
    test_url = input("Enter Salad storage URL to transcribe: ")
    
    print("Salad API Transcription Test")
    print("-" * 30)
    
    result = request_transcription(test_url)
    
    if result:
        print("\nFull API Response:")
        print("-" * 20)
        for key, value in result.items():
            print(f"{key}: {value}")
        
        # Check job status if job ID is available
        job_id = result.get('id')
        if job_id:
            status = check_job_status(job_id)
            if status:
                print("\nJob Status Details:")
                print("-" * 20)
                for key, value in status.items():
                    print(f"{key}: {value}")