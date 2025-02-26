import os
import requests
from pathlib import Path
import json
import argparse
from dotenv import load_dotenv

def download_from_salad(url, output_dir="./transcripts", filename=None):
    """
    Download a file from Salad storage using a signed URL.
    
    Args:
        url (str): The signed URL to download the file from
        output_dir (str): Directory to save the downloaded file (default: "./transcripts")
        filename (str): Optional filename to use for the downloaded file
                        If not provided, will extract from URL or use a default name
    
    Returns:
        str: Path to the downloaded file if successful, None otherwise
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract filename from URL if not provided
        if not filename:
            # Try to extract filename from URL
            url_path = url.split('?')[0]  # Remove query parameters
            url_filename = url_path.split('/')[-1]
            
            if url_filename and '.' in url_filename:
                filename = url_filename
            else:
                # If URL doesn't contain a proper filename, use a default
                filename = "transcription.json"
        
        # Full path for the output file
        output_path = os.path.join(output_dir, filename)
        
        print(f"Downloading from: {url}")
        print(f"Saving to: {output_path}")
        
        # Download the file
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            
            # Get content type to determine file format
            content_type = response.headers.get('Content-Type', '')
            
            # If content type is JSON but filename doesn't reflect that, adjust filename
            if 'json' in content_type.lower() and not filename.endswith('.json'):
                output_path = f"{output_path}.json"
                print(f"Content is JSON, adjusted filename to: {output_path}")
            
            # Save the file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        print(f"✓ Download successful!")
        
        # If it's a JSON file, try to parse and display some info
        if output_path.endswith('.json'):
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Display summary of the transcription
                print("\nTranscription Summary:")
                print("-" * 30)
                
                if isinstance(data, dict):
                    if 'segments' in data:
                        segments = data['segments']
                        print(f"Total segments: {len(segments)}")
                        if segments:
                            print(f"First segment: {segments[0].get('text', '')[:100]}...")
                            print(f"Last segment: {segments[-1].get('text', '')[:100]}...")
                    elif 'text' in data:
                        print(f"Full text length: {len(data['text'])} characters")
                        print(f"Preview: {data['text'][:100]}...")
                elif isinstance(data, list) and len(data) > 0:
                    print(f"Total entries: {len(data)}")
                    if 'text' in data[0]:
                        print(f"First entry: {data[0]['text'][:100]}...")
                        print(f"Last entry: {data[-1]['text'][:100]}...")
            except Exception as e:
                print(f"Note: Could not parse JSON content: {str(e)}")
        
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Download failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text[:200]}")  # Show first 200 chars of error
        return None
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return None

def main():
    """Command line interface for downloading from Salad storage"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Download files from Salad storage")
    parser.add_argument("--url", type=str, help="Signed URL to download from")
    parser.add_argument("--output-dir", type=str, default="./transcripts", 
                        help="Directory to save downloaded files (default: ./transcripts)")
    parser.add_argument("--filename", type=str, help="Filename to use for the downloaded file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If URL is not provided as argument, use the default test URL
    url = args.url or "https://storage-api.salad.com/organizations/salad/files/transcription/ee8a1ae2-5f31-4642-9b0a-cd25de655b98?token=184f86e0-5325-480a-a698-21e30acaa5e8"
    
    # Download the file
    output_path = download_from_salad(url, args.output_dir, args.filename)
    
    if output_path:
        print(f"\nFile downloaded successfully to: {output_path}")
    else:
        print("\nDownload failed.")

if __name__ == "__main__":
    main()