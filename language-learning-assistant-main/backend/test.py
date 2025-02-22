from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def explore_transcript_options(video_id: str):
    """Explore all available transcript options for a video."""
    try:
        # Get list of available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        print(f"\nTranscript Options for video {video_id}:")
        print("-" * 50)
        
        # Get all available transcripts
        print("\nAvailable Transcripts:")
        for transcript in transcript_list:
            print(f"Language: {transcript.language} ({transcript.language_code})")
            print(f"Is generated: {transcript.is_generated}")
            print(f"Is translatable: {transcript.is_translatable}")
            print("-" * 30)
            
        # Try to get default transcript
        print("\nAttempting to get default transcript...")
        transcript = transcript_list.find_transcript(['en'])
        print(f"Default transcript language: {transcript.language}")
        print(f"Default transcript language code: {transcript.language_code}")
        print(f"Is translation: {transcript.is_translation}")
        print(f"Is generated: {transcript.is_generated}")
        
        # Try to get available translations
        print("\nAvailable translations:")
        translation_languages = transcript.translation_languages
        for lang in translation_languages:
            print(f"Language: {lang['language']} ({lang['language_code']})")

        # Test transcript download with timestamp
        print("\nTesting transcript download with timestamp...")
        transcript_with_time = YouTubeTranscriptApi.get_transcript(video_id)
        if transcript_with_time:
            print("Successfully downloaded transcript with timestamp")
            print(f"First few entries:")
            for entry in transcript_with_time[:3]:
                print(f"Time: {entry['start']}-{entry['start'] + entry['duration']}, Text: {entry['text']}")
            
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video")
    except NoTranscriptFound:
        print("No transcripts were found for this video")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Test with a few different videos
    test_videos = [
        "dQw4w9WgXcQ",  # Known video with transcripts
        "jNQXAC9IVRw",  # First YouTube video
        "UC_x5XG1OV2P6uZZ5FSM9Ttw",  # A channel ID (should fail)
        "WU5ls6mQ35s"  # Video requiring timestamp workaround
    ]
    
    for video_id in test_videos:
        print(f"\nTesting video ID: {video_id}")
        print("=" * 50)
        explore_transcript_options(video_id)

if __name__ == "__main__":
    main()