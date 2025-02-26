import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
SALAD_API_KEY = os.getenv("SALAD_API_KEY", "").strip()
SALAD_ORGANIZATION_NAME = os.getenv("SALAD_ORGANIZATION_NAME", "").strip()

# Test URLs for audio files
# url1 = "https://storage-api.salad.com/organizations/moztst/files/audio/cLZMED4rlgY.mp3?token=4030d5e5-84f9-409f-a965-3fc88f943aff"
# url2 = "https://storage-api.salad.com/organizations/moztst/files/audio/DjxgpzIeiws.mp3?token=7eedb263-f2ae-477c-9b41-8ab894c4f37c"

def check_job_status(job_id, organization_name=None, api_key=None):
    """
    Check the status of a transcription job.
    
    Args:
        job_id (str): The ID of the transcription job
        organization_name (str): Salad organization name (optional)
        api_key (str): Salad API key (optional)
        
    Returns:
        dict: Job status information
    """
    try:
        # Get credentials from environment variables if not provided
        organization_name = organization_name or SALAD_ORGANIZATION_NAME
        api_key = api_key or SALAD_API_KEY
        
        if not organization_name or not api_key:
            raise ValueError("Missing required credentials")
            
        # Prepare API request
        endpoint = f"https://api.salad.com/api/public/organizations/{organization_name}/inference-endpoints/transcribe/jobs/{job_id}"
        
        headers = {
            "Salad-Api-Key": api_key
        }
        
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error checking job status: {e}")
        return None

def download_subtitles(job_id, output_dir="./subtitles", organization_name=None, api_key=None):
    """
    Download the subtitles for a completed transcription job.
    
    Args:
        job_id (str): The ID of the transcription job
        output_dir (str): Directory to save the subtitles file
        organization_name (str): Salad organization name (optional)
        api_key (str): Salad API key (optional)
        
    Returns:
        str: Path to the downloaded subtitles file
    """
    try:
        # Get credentials from environment variables if not provided
        organization_name = organization_name or SALAD_ORGANIZATION_NAME
        api_key = api_key or SALAD_API_KEY
        
        if not organization_name or not api_key:
            raise ValueError("Missing required credentials")
            
        # Check job status first
        status = check_job_status(job_id, organization_name, api_key)
        if not status or status.get("status") not in ["completed", "succeeded"]:
            raise ValueError(f"Job {job_id} is not completed or succeeded")
            
        # Get the output URL from the job status
        output_url = status.get("output", {}).get("url")
        if not output_url:
            raise ValueError("No output URL found in job status")
            
        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download the subtitles file
        response = requests.get(output_url)
        response.raise_for_status()
        
        # Save to file
        output_file = output_dir / f"{job_id}.srt"
        with open(output_file, "wb") as f:
            f.write(response.content)
            
        print(f"\n✓ Subtitles downloaded to: {output_file}")
        return str(output_file)
        
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error downloading subtitles: {e}")
        return None

def monitor_job(job_id, check_interval=10, max_attempts=30):
    """
    Monitor a transcription job until it completes or fails.
    
    Args:
        job_id (str): The ID of the transcription job
        check_interval (int): Time in seconds between status checks
        max_attempts (int): Maximum number of status checks
        
    Returns:
        bool: True if job completed successfully, False otherwise
    """
    print(f"\nMonitoring job {job_id}...")
    
    for attempt in range(max_attempts):
        status = check_job_status(job_id)
        if not status:
            print("Failed to get job status")
            return False
            
        job_status = status.get("status")
        print(f"Status: {job_status} (attempt {attempt + 1}/{max_attempts})")
        
        if job_status in ["completed", "succeeded"]:
            print("\n✓ Job completed successfully!")
            return True
        elif job_status in ["failed", "cancelled"]:
            print(f"\n✗ Job {job_status}")
            return False
            
        time.sleep(check_interval)
    
    print("\n✗ Monitoring timed out")
    return False

def main():
    """
    Main function to test job monitoring and subtitle downloading.
    """
    # Example job ID - replace with actual job ID from transcription request
    job_id = input("Enter the job ID to monitor: ")
    
    if monitor_job(job_id):
        # Download subtitles if job completed successfully
        subtitle_file = download_subtitles(job_id)
        if subtitle_file:
            print(f"Process completed successfully. Subtitles saved to: {subtitle_file}")
    else:
        print("Job monitoring failed or timed out")

if __name__ == "__main__":
    main()
