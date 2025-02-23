import os
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

def upload_to_s3(audio_file_path, bucket_name, s3_key=None):
    """
    Uploads an audio file to S3 and generates a presigned URL for access.

    Args:
        audio_file_path (str): Path to the audio file
        bucket_name (str): Name of the S3 bucket
        s3_key (str): Key for the file in S3 (if None, uses filename)

    Returns:
        str: Presigned URL for the uploaded file
    """
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3')

        # If no S3 key provided, use the filename
        if not s3_key:
            s3_key = f"audio/{Path(audio_file_path).name}"

        # Upload file to S3
        print(f"\nUploading {Path(audio_file_path).name} to S3...")
        with open(audio_file_path, 'rb') as file:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                s3_key,
                ExtraArgs={'ContentType': 'audio/mpeg'}
            )

        # Generate presigned URL (valid for 3 days)
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=3 * 24 * 60 * 60  # 3 days in seconds
        )

        return presigned_url

    except ClientError as e:
        print(f"Error uploading to S3: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def test_s3_upload():
    """
    Test function to validate S3 upload functionality.
    """
    # Load environment variables
    load_dotenv()

    # Get S3 credentials from environment variables
    bucket_name = os.getenv("S3_BUCKET_NAME")

    if not bucket_name:
        print("Error: Missing required environment variable S3_BUCKET_NAME")
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
        presigned_url = upload_to_s3(
            str(mp3_file),
            bucket_name
        )

        if presigned_url:
            print(f"Successfully uploaded {mp3_file.name}")
            print(f"Presigned URL: {presigned_url}")
        else:
            print(f"Failed to upload {mp3_file.name}")

if __name__ == "__main__":
    test_s3_upload()