#!/usr/bin/env python3
"""
Test script to check the status of a Salad transcription job independently.
This helps verify if the API is returning correct status information.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
SALAD_API_KEY = os.getenv("SALAD_API_KEY", "").strip()
SALAD_ORGANIZATION_NAME = os.getenv("SALAD_ORGANIZATION_NAME", "").strip()

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
            print("Error: Missing required credentials. Set SALAD_ORGANIZATION_NAME and SALAD_API_KEY environment variables")
            return None
            
        # Clean and validate organization name
        organization_name = organization_name.strip()
        
        # Prepare API request
        endpoint = f"https://api.salad.com/api/public/organizations/{organization_name}/inference-endpoints/transcribe/jobs/{job_id}"
        
        headers = {
            "Salad-Api-Key": api_key
        }
        
        # Send status request
        print(f"Checking status for job {job_id}...")
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"Job status: {result.get('status')}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def main():
    """Main function to run the test."""
    if len(sys.argv) < 2:
        print("Usage: python test_job_status.py <job_id>")
        return
    
    job_id = sys.argv[1]
    print(f"Testing job status for job ID: {job_id}")
    
    # Check job status
    status = check_job_status(job_id)
    
    if status:
        # Print the full response in a formatted way
        print("\nFull API Response:")
        print("-" * 50)
        print(json.dumps(status, indent=2))
        
        # Print specific fields of interest
        print("\nKey Information:")
        print("-" * 50)
        print(f"Status: {status.get('status')}")
        print(f"Create Time: {status.get('create_time')}")
        print(f"Update Time: {status.get('update_time')}")
        
        # Print events if they exist
        if 'events' in status and status['events']:
            print("\nEvents:")
            print("-" * 50)
            for i, event in enumerate(status['events']):
                print(f"Event {i+1}:")
                print(f"  Action: {event.get('action')}")
                print(f"  Time: {event.get('time')}")
        
        # Print output information if available
        if 'output' in status and status['output']:
            print("\nOutput:")
            print("-" * 50)
            print(f"URL: {status['output'].get('url')}")
    else:
        print("Failed to get job status.")

if __name__ == "__main__":
    main()