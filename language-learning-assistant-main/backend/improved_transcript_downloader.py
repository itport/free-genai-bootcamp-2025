from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, List, Dict, Tuple, Any
import os
import streamlit as st

class ImprovedTranscriptDownloader:
    def __init__(self, languages: List[str] = ["ro", "en"]):
        """Initialize ImprovedTranscriptDownloader with specified languages
        
        Args:
            languages (List[str]): List of language codes to try when downloading transcripts.
                                  Defaults to Romanian and English.
        """
        self.languages = languages

    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        if "v=" in url:
            return url.split("v=")[1].split("&")[0][:11]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0][:11]
        return None

    def get_transcript(self, video_id: str, use_fallback: bool = True, languages: List[str] = None) -> Optional[List[Dict]]:
        """
        Download YouTube Transcript
        
        Args:
            video_id (str): YouTube video ID or URL
            use_fallback (bool): Whether to use any available language if preferred languages aren't available
            languages (List[str]): Optional list of language codes to override the default languages
            
        Returns:
            Optional[List[Dict]]: Transcript if successful, None otherwise
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)
            
        if not video_id:
            print("Invalid video ID or URL")
            return None

        print(f"Downloading transcript for video ID: {video_id}")
        
        # Use provided languages or default to self.languages
        lang_list = languages if languages is not None else self.languages
        
        try:
            # First try with specified languages
            return YouTubeTranscriptApi.get_transcript(video_id, languages=lang_list)
        except Exception as e:
            print(f"An error occurred with specified languages {lang_list}: {str(e)}")
            
            # If fallback is enabled, try to get any available transcript
            if use_fallback:
                try:
                    print("Trying fallback: Getting list of available transcripts...")
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    
                    # Get the first available transcript (generated or manual)
                    for transcript in transcript_list:
                        print(f"Found transcript in {transcript.language_code} ({transcript.language})")
                        print(f"Is generated: {transcript.is_generated}")
                        
                        # Get the transcript data
                        transcript_data = transcript.fetch()
                        print(f"Successfully retrieved transcript in {transcript.language_code}")
                        return transcript_data
                        
                except Exception as fallback_error:
                    print(f"Fallback also failed: {str(fallback_error)}")
            
            return None

    def list_available_transcripts(self, video_id: str) -> List[str]:
        """
        Get a list of available transcript language codes for a video
        
        Args:
            video_id (str): YouTube video ID or URL
            
        Returns:
            List[str]: List of language codes available for the video
        """
        # Extract video ID if full URL is provided
        if "youtube.com" in video_id or "youtu.be" in video_id:
            video_id = self.extract_video_id(video_id)
            
        if not video_id:
            print("Invalid video ID or URL")
            return []

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Collect manually created transcripts first
            manual_langs = []
            generated_langs = []
            
            for transcript in transcript_list:
                if transcript.is_generated:
                    generated_langs.append(transcript.language_code)
                else:
                    manual_langs.append(transcript.language_code)
                    
            # Return manually created first, then generated
            return manual_langs + generated_langs
            
        except Exception as e:
            print(f"Error listing available transcripts: {str(e)}")
            return []

    def save_transcript(self, transcript: List[Dict], filename: str) -> bool:
        """
        Save transcript to file
        
        Args:
            transcript (List[Dict]): Transcript data
            filename (str): Output filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Ensure translations directory exists
        os.makedirs("./transcripts", exist_ok=True)
        filename = f"./transcripts/{filename}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            return True
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False

    def download_transcript_with_ui(self, url: str) -> Dict[str, Any]:
        """
        Download transcript with improved UI feedback
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Dict: Result with success status, message, and transcript data if successful
        """
        result = {
            "success": False,
            "message": "",
            "transcript": None,
            "transcript_text": None,
            "video_id": None
        }
        
        try:
            # Extract video ID
            video_id = self.extract_video_id(url)
            if not video_id:
                result["message"] = "Invalid YouTube URL or unable to extract video ID"
                return result
                
            result["video_id"] = video_id
            
            # First try to get transcript with default languages (ro, en) without fallback
            with st.spinner(f"Downloading transcript for video ID: {video_id}..."):
                transcript = self.get_transcript(video_id, use_fallback=False)
                
                if transcript:
                    # Save transcript and update result
                    if self.save_transcript(transcript, video_id):
                        transcript_text = "\n".join([entry['text'] for entry in transcript])
                        result["success"] = True
                        result["message"] = f"Transcript downloaded and saved as {video_id}.txt!"
                        result["transcript"] = transcript
                        result["transcript_text"] = transcript_text
                    else:
                        result["message"] = "Failed to save the transcript."
                else:
                    # Get available languages for this video
                    available_langs = self.list_available_transcripts(video_id)
                    
                    if available_langs:
                        result["message"] = f"No transcript found in Romanian or English. Available languages: {', '.join(available_langs)}"
                        result["available_languages"] = available_langs
                    else:
                        result["message"] = "No transcripts available for this video. Consider using the audio download and transcription option instead."
        
        except Exception as e:
            result["message"] = f"Error downloading transcript: {str(e)}"
        
        return result