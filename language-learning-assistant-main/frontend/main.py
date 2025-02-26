from youtube_transcript_api import YouTubeTranscriptApi
import re
import os

class YouTubeTranscriptDownloader:
    def __init__(self):
        self.transcript_dir = "transcripts"
        os.makedirs(self.transcript_dir, exist_ok=True)

    def extract_video_id(self, url):
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
            r'(?:embed\/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def get_transcript(self, url):
        """Get transcript with fallback options."""
        video_id = self.extract_video_id(url)
        if not video_id:
            return None

        try:
            # Try Romanian manual transcripts first
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['ro']
            )
            return transcript
        except:
            try:
                # Try Romanian auto-generated transcripts
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=['ro-RO']
                )
                return transcript
            except:
                try:
                    # Fall back to English transcripts
                    transcript = YouTubeTranscriptApi.get_transcript(
                        video_id,
                        languages=['en']
                    )
                    return transcript
                except:
                    return None

    def save_transcript(self, transcript, video_id):
        """Save transcript to file.
        
        Args:
            transcript: List of transcript entries
            video_id: YouTube video ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            filepath = os.path.join(self.transcript_dir, f"{video_id}.txt") 
            with open(filepath, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['text']}\n")
            return True
        except Exception:
            return False
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from typing import Dict
import json
from collections import Counter
import re

from backend.chat import SambanovaChat
# Commenting out the problematic import and using the local implementation instead
# from backend.get_transcript_with_fallback import YouTubeTranscriptDownloader
from backend.improved_transcript_downloader import ImprovedTranscriptDownloader
from backend.video_downloader import YouTubeVideoDownloader


# Page config
st.set_page_config(
    page_title="Romanian Learning Assistant",
    page_icon="🇷🇴",
    layout="wide"
)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize additional session state variables
if 'download_complete' not in st.session_state:
    st.session_state.download_complete = False
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'upload_requested' not in st.session_state:
    st.session_state.upload_requested = False
if 'upload_result' not in st.session_state:
    st.session_state.upload_result = None

# Initialize session state variables for transcription
if 'transcription_job' not in st.session_state:
    st.session_state.transcription_job = None
if 'transcription_requested' not in st.session_state:
    st.session_state.transcription_requested = False

def on_transcription_request(signed_url, transcription_params=None):
    """Handle the transcription request button click"""
    st.session_state.transcription_requested = True
    st.session_state.transcription_url = signed_url
    st.session_state.transcription_params = transcription_params or {}

def perform_transcription_request():
    """Perform the actual transcription request"""
    if not st.session_state.transcription_requested:
        return
    
    # Reset the flag
    st.session_state.transcription_requested = False
    
    signed_url = st.session_state.transcription_url
    transcription_params = st.session_state.transcription_params
    
    try:
        # Import the transcription module
        from backend.salad_transcribe import request_transcription
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Get credentials
        import os
        salad_api_key = os.getenv("SALAD_API_KEY")
        organization_name = os.getenv("SALAD_ORGANIZATION_NAME")
        
        if not salad_api_key or not organization_name:
            st.session_state.transcription_job = {
                "success": False,
                "message": "Missing Salad API credentials in environment variables"
            }
            return
        
        with st.spinner("Requesting transcription..."):
            # Call the transcription function with parameters
            result = request_transcription(
                signed_url,
                organization_name,
                salad_api_key,
                **transcription_params
            )
            
            if result and "error" not in result:
                st.session_state.transcription_job = {
                    "success": True,
                    "message": "Transcription job submitted successfully!",
                    "job_id": result.get("id"),
                    "details": result
                }
            else:
                error_message = result.get("error") if result else "Unknown error"
                st.session_state.transcription_job = {
                    "success": False,
                    "message": f"Failed to submit transcription job: {error_message}"
                }
    except Exception as e:
        st.session_state.transcription_job = {
            "success": False,
            "message": f"Error requesting transcription: {str(e)}"
        }

def on_download_click(url, format_option):
    """Handle the download button click"""
    try:
        with st.spinner("Downloading and processing video..."):
            # Store the original URL for later use
            st.session_state.original_url = url
            
            # Import required modules here to ensure they're available
            from dotenv import load_dotenv
            from backend.test_salad_upload import upload_to_salad_storage
            
            video_downloader = YouTubeVideoDownloader()
            # First extract video info to show progress
            video_id = video_downloader.extract_video_id(url)
            if not video_id:
                st.error("Invalid YouTube URL or unable to extract video ID")
                return
                
            st.info(f"Processing video ID: {video_id}")
            # Use download_audio for mp3, download_video for original
            if format_option == "mp3":
                video_path = video_downloader.download_audio(url)
            else:
                video_path = video_downloader.download_video(url)
            
            if video_path:
                # Convert to absolute path if needed
                # Get the filename from the path
                filename = os.path.basename(video_path)
                # Ensure we have an absolute path
                video_path = os.path.abspath(video_path)
                
                # Store in session state
                st.session_state.download_complete = True
                st.session_state.video_path = video_path
                st.session_state.filename = filename
                st.session_state.audio_path = video_path
                st.session_state.video_id = video_id  # Store the video ID
                
                return True
            else:
                # Display the specific error message from the backend
                st.error("Failed to download and process the video. Please check the following possible issues:\n" +
                        "1. Video availability and accessibility\n" +
                        "2. Audio format availability\n" +
                        "3. Disk space and permissions\n" +
                        "4. FFmpeg installation for audio conversion")
                return False
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        return False

def on_upload_click(storage_option):
    """Handle the upload button click"""
    st.session_state.upload_requested = True
    st.session_state.selected_storage = storage_option

def perform_upload():
    """Perform the actual upload operation"""
    if not st.session_state.upload_requested:
        return
    
    # Reset the flag
    st.session_state.upload_requested = False
    
    storage_option = st.session_state.selected_storage
    video_path = st.session_state.video_path
    filename = st.session_state.filename
    
    if storage_option == "Salad":
        try:
            # Import required modules
            from dotenv import load_dotenv
            from backend.test_salad_upload import upload_to_salad_storage
            
            # Load environment variables
            load_dotenv()
            
            # Get credentials
            salad_api_key = os.getenv("SALAD_API_KEY")
            organization_name = os.getenv("SALAD_ORGANIZATION_NAME")
            
            if not salad_api_key or not organization_name:
                st.session_state.upload_result = {
                    "success": False,
                    "message": "Missing Salad API credentials in environment variables"
                }
                return
            
            # Determine MIME type based on file extension
            mime_type = "audio/mpeg"  # Default for mp3
            if video_path.lower().endswith('.mp4'):
                mime_type = "video/mp4"
            elif video_path.lower().endswith('.webm'):
                mime_type = "video/webm"
            elif video_path.lower().endswith('.wav'):
                mime_type = "audio/wav"
            
            with st.spinner(f"Uploading {filename} to Salad storage..."):
                # Call the upload function with the correct parameters
                signed_url = upload_to_salad_storage(
                    video_path,  # Full path to the file
                    salad_api_key,
                    organization_name,
                    mime_type=mime_type
                )
                
                if signed_url:
                    # Store the URL in session state for later use
                    if 'uploaded_files' not in st.session_state:
                        st.session_state.uploaded_files = {}
                    st.session_state.uploaded_files[filename] = {
                        'path': video_path,
                        'url': signed_url,
                        'service': 'Salad'
                    }
                    
                    st.session_state.upload_result = {
                        "success": True,
                        "message": f"Successfully uploaded to Salad storage!",
                        "url": signed_url
                    }
                else:
                    st.session_state.upload_result = {
                        "success": False,
                        "message": "Failed to upload to Salad storage. Check the logs for details."
                    }
        except Exception as e:
            st.session_state.upload_result = {
                "success": False,
                "message": f"Error during upload: {str(e)}"
            }
    elif storage_option == "AWS S3":
        st.session_state.upload_result = {
            "success": False,
            "message": "AWS S3 upload functionality will be implemented soon"
        }
    else:  # Google Cloud
        st.session_state.upload_result = {
            "success": False,
            "message": "Google Cloud upload functionality will be implemented soon"
        }

def render_header():
    """Render the header section"""
    st.title("Romanian Learning Assistant")
    st.markdown("""
    Transform YouTube transcripts into interactive Romanian learning experiences.
    
    This tool demonstrates:
    - DeepSeek-R1 Language Model Integration
    - RAG (Retrieval Augmented Generation)
    - Structured Learning Approach
    - Agent-based Learning Systems
    """)

def render_sidebar():
    """Render the sidebar with component selection"""
    with st.sidebar:
        st.header("Development Stages")
        
        # Main component selection
        selected_stage = st.radio(
            "Select Stage:",
            [
                "1. Chat with DeepSeek-R1",
                "2. Raw Transcript",
                "3. Video to Subtitles",
                "4. Structured Data",
                "5. RAG Implementation",
                "6. Interactive Learning"
            ]
        )
        
        # Stage descriptions
        stage_info = {
            "1. Chat with DeepSeek-R1": """
            **Current Focus:**
            - Basic Romanian learning
            - Advanced language understanding
            - Interactive conversations
            """,
            
            "2. Raw Transcript": """
            **Current Focus:**
            - YouTube transcript download
            - Raw text visualization
            - Initial data examination
            """,
            
            "3. Video to Subtitles": """
            **Current Focus:**
            - Video download and processing
            - Audio extraction
            - Subtitle generation
            """,
            
            "4. Structured Data": """
            **Current Focus:**
            - Text cleaning
            - Dialogue extraction
            - Data structuring
            """,
            
            "5. RAG Implementation": """
            **Current Focus:**
            - Bedrock embeddings
            - Vector storage
            - Context retrieval
            """,
            
            "6. Interactive Learning": """
            **Current Focus:**
            - Scenario generation
            - Audio synthesis
            - Interactive practice
            """
        }
        
        st.markdown("---")
        st.markdown(stage_info[selected_stage])
        
        return selected_stage

def render_chat_stage():
    """Render an improved chat interface"""
    st.header("Chat with DeepSeek-R1")

    # Initialize SambanovaChat instance if not in session state
    if 'sambanova_chat' not in st.session_state:
        st.session_state.sambanova_chat = SambanovaChat()

    # Introduction text
    st.markdown("""
    Start by exploring DeepSeek-R1's Romanian language capabilities. Try asking questions about Romanian grammar, 
    vocabulary, or cultural aspects.
    """)

    # Initialize chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

    # Chat input area
    if prompt := st.chat_input("Ask about Romanian language..."):
        # Process the user input
        process_message(prompt)

    # Example questions in sidebar
    with st.sidebar:
        st.markdown("### Try These Examples")
        example_questions = [
            "How do I say 'Where is the train station?' in Romanian?",
            "Explain the difference between 'sunt' and 'este'",
            "What's the polite form of 'a mânca'?",
            "How do I count objects in Romanian?",
            "What's the difference between 'bună dimineața' and 'bună seara'?",
            "How do I ask for directions politely?"
        ]
        
        for q in example_questions:
            if st.button(q, use_container_width=True, type="secondary"):
                # Process the example question
                process_message(q)
                st.rerun()

    # Add a clear chat button
    if st.session_state.messages:
        if st.button("Clear Chat", type="primary"):
            st.session_state.messages = []
            st.rerun()

def process_message(prompt: str):
    """Process a user message and generate a response"""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create a placeholder for the assistant's response
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream the response
        for chunk in st.session_state.sambanova_chat.generate_stream(prompt):
            full_response += chunk
            # Show the complete response in the main message area
            message_placeholder.markdown(full_response)

        # Ensure the final complete response is displayed
        message_placeholder.markdown(full_response)

    # Add assistant's message to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})



def count_characters(text):
    """Count Romanian and total characters in text"""
    if not text:
        return 0, 0
        
    def is_romanian(char):
        return any([
            char in 'ăâîșțĂÂÎȘȚ',  # Romanian special characters
            'a' <= char.lower() <= 'z',  # Basic Latin alphabet
            char.isspace() or char in ',.!?-'  # Common punctuation
        ])
    
    ro_chars = sum(1 for char in text if is_romanian(char))
    return ro_chars, len(text)

def render_transcript_stage():
    """Render the raw transcript stage"""
    st.header("Raw Transcript Processing")
    
    # URL input
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Romanian lesson YouTube URL"
    )
    
    # Download buttons and processing
    if url:
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            if st.button("Download Transcript"):
                try:
                    downloader = YouTubeTranscriptDownloader()
                    transcript = downloader.get_transcript(url)
                    if transcript:
                        # Extract video ID and save transcript
                        video_id = downloader.extract_video_id(url)
                        if video_id and downloader.save_transcript(transcript, video_id):
                            # Store the raw transcript text in session state
                            transcript_text = "\n".join([entry['text'] for entry in transcript])
                            st.session_state.transcript = transcript_text
                            st.success(f"Transcript downloaded and saved as {video_id}.txt!")
                        else:
                            st.error("Failed to save the transcript.")
                    else:
                        st.error("No transcript found for this video.")
                except Exception as e:
                    st.error(f"Error downloading transcript: {str(e)}")
        
        with col_download2:
            if st.button("Download Audio"):
                try:
                    video_downloader = YouTubeVideoDownloader()
                    video_path = video_downloader.download_video(url)
                    if video_path:
                        st.success(f"Audio downloaded successfully to {video_path}!")
                    else:
                        st.error("Failed to download the audio.")
                except Exception as e:
                    st.error(f"Error downloading audio: {str(e)}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Raw Transcript")
        if st.session_state.transcript:
            st.text_area(
                label="Raw text",
                value=st.session_state.transcript,
                height=400,
                disabled=True
            )
        else:
            st.info("No transcript loaded yet")
    
    with col2:
        st.subheader("Transcript Stats")
        if st.session_state.transcript:
            # Calculate stats
            jp_chars, total_chars = count_characters(st.session_state.transcript)
            total_lines = len(st.session_state.transcript.split('\n'))
            
            # Display stats
            st.metric("Total Characters", total_chars)
            st.metric("Romanian Characters", jp_chars)
            st.metric("Total Lines", total_lines)
        else:
            st.info("Load a transcript to see statistics")

def render_video_subtitles_stage():
    """Render the video to subtitles stage"""
    st.header("Video to Subtitles")
    
    # Check if we need to perform an upload (from a previous interaction)
    if st.session_state.upload_requested:
        perform_upload()
    
    # Check if we need to perform a transcription request
    if st.session_state.transcription_requested:
        perform_transcription_request()
    
    # Display upload result if available
    if st.session_state.upload_result:
        if st.session_state.upload_result["success"]:
            st.success(st.session_state.upload_result["message"])
            
            # Display the signed URL
            signed_url = st.session_state.upload_result["url"]
            st.markdown(f"**Signed URL:** {signed_url}")
            
            # Initialize transcription parameters page if not in session state
            if 'transcription_page' not in st.session_state:
                st.session_state.transcription_page = 1
            
            # Add transcription parameters section
            st.subheader("Transcription Parameters")
            
            # Create page navigation
            col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
            with col_nav1:
                if st.session_state.transcription_page > 1:
                    if st.button("← Previous", use_container_width=True):
                        st.session_state.transcription_page -= 1
                        st.rerun()
            
            with col_nav2:
                st.markdown(f"### Page {st.session_state.transcription_page} of 3")
            
            with col_nav3:
                if st.session_state.transcription_page < 3:
                    if st.button("Next →", use_container_width=True):
                        st.session_state.transcription_page += 1
                        st.rerun()
            
            # Initialize parameters dictionary if not in session state
            if 'transcription_params_dict' not in st.session_state:
                st.session_state.transcription_params_dict = {
                    "return_as_file": True,
                    "language_code": "en",
                    "translate": "none",
                    "sentence_level_timestamps": True,
                    "word_level_timestamps": True,
                    "diarization": True,
                    "sentence_diarization": True,
                    "srt": True,
                    "summarize": 100,
                    "llm_translation": [],
                    "srt_translation": [],
                    "custom_vocabulary": "",
                    "webhook": "",
                    "job_metadata": ""
                }
            
            # Page 1: Basic Parameters
            if st.session_state.transcription_page == 1:
                st.markdown("### Basic Parameters")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Language selection
                    st.session_state.transcription_params_dict["language_code"] = st.selectbox(
                        "Language Code",
                        ["en", "ro", "fr", "de", "es", "it", "pt", "hi", "th"],
                        index=["en", "ro", "fr", "de", "es", "it", "pt", "hi", "th"].index(
                            st.session_state.transcription_params_dict["language_code"]
                        )
                    )
                    
                    # Translation option
                    translate_options = ["none", "to_eng"]
                    translate_display = ["No translation", "Translate to English"]
                    
                    st.session_state.transcription_params_dict["translate"] = st.selectbox(
                        "Translate",
                        translate_options,
                        index=translate_options.index(st.session_state.transcription_params_dict["translate"]),
                        format_func=lambda x: translate_display[translate_options.index(x)]
                    )
                
                with col2:
                    # File return option
                    st.session_state.transcription_params_dict["return_as_file"] = st.checkbox(
                        "Return as file", 
                        value=st.session_state.transcription_params_dict["return_as_file"]
                    )
                    
                    # Summarization
                    st.session_state.transcription_params_dict["summarize"] = st.number_input(
                        "Summarize (words)", 
                        min_value=0, 
                        value=st.session_state.transcription_params_dict["summarize"],
                        help="Number of words for summary (0 to disable)"
                    )
                
                st.markdown("---")
                st.info("Navigate to the next page to configure timestamp and diarization options.")
            
            # Page 2: Timestamp and Diarization Options
            elif st.session_state.transcription_page == 2:
                st.markdown("### Timestamp & Diarization Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Timestamp Options")
                    st.session_state.transcription_params_dict["sentence_level_timestamps"] = st.checkbox(
                        "Sentence-level timestamps", 
                        value=st.session_state.transcription_params_dict["sentence_level_timestamps"]
                    )
                    
                    st.session_state.transcription_params_dict["word_level_timestamps"] = st.checkbox(
                        "Word-level timestamps", 
                        value=st.session_state.transcription_params_dict["word_level_timestamps"]
                    )
                    
                    # Output format options
                    st.subheader("Output Options")
                    st.session_state.transcription_params_dict["srt"] = st.checkbox(
                        "Generate SRT", 
                        value=st.session_state.transcription_params_dict["srt"]
                    )
                
                with col2:
                    # Diarization options
                    st.subheader("Diarization Options")
                    st.info("Diarization identifies different speakers in the audio.")
                    
                    st.session_state.transcription_params_dict["diarization"] = st.checkbox(
                        "Speaker diarization", 
                        value=st.session_state.transcription_params_dict["diarization"]
                    )
                    
                    st.session_state.transcription_params_dict["sentence_diarization"] = st.checkbox(
                        "Sentence diarization", 
                        value=st.session_state.transcription_params_dict["sentence_diarization"]
                    )
                
                st.markdown("---")
                st.info("Navigate to the next page to configure advanced options like translations and webhooks.")
            
            # Page 3: Advanced Options
            else:
                st.markdown("### Advanced Options")
                
                # Translation options
                st.subheader("Translation Options")
                
                all_languages = ["german", "italian", "french", "spanish", "english", "portuguese", "hindi", "thai"]
                
                st.session_state.transcription_params_dict["llm_translation"] = st.multiselect(
                    "LLM Translation Languages",
                    all_languages,
                    default=st.session_state.transcription_params_dict["llm_translation"]
                )
                
                st.session_state.transcription_params_dict["srt_translation"] = st.multiselect(
                    "SRT Translation Languages",
                    all_languages,
                    default=st.session_state.transcription_params_dict["srt_translation"]
                )
                
                # Custom vocabulary
                st.subheader("Additional Options")
                st.session_state.transcription_params_dict["custom_vocabulary"] = st.text_input(
                    "Custom Vocabulary",
                    value=st.session_state.transcription_params_dict["custom_vocabulary"],
                    placeholder="Enter terms divided by commas",
                    help="Specialized terms to improve transcription accuracy"
                )
                
                # Webhook and metadata
                st.session_state.transcription_params_dict["webhook"] = st.text_input(
                    "Webhook URL",
                    value=st.session_state.transcription_params_dict["webhook"],
                    placeholder="https://your-webhook-url.com",
                    help="URL to receive job completion notifications"
                )
                
                st.session_state.transcription_params_dict["job_metadata"] = st.text_area(
                    "Job Metadata (JSON)",
                    value=st.session_state.transcription_params_dict["job_metadata"],
                    placeholder='{"my-job-id": 1234}',
                    help="Custom metadata for this job in JSON format"
                )
            
            # Show summary of selected options
            with st.expander("View Selected Parameters"):
                # Create a readable summary of the parameters
                params_summary = {
                    "Language": st.session_state.transcription_params_dict["language_code"],
                    "Translation": "None" if st.session_state.transcription_params_dict["translate"] == "none" else "To English",
                    "Return as file": "Yes" if st.session_state.transcription_params_dict["return_as_file"] else "No",
                    "Summarize": f"{st.session_state.transcription_params_dict['summarize']} words" if st.session_state.transcription_params_dict["summarize"] > 0 else "No",
                    "Sentence timestamps": "Yes" if st.session_state.transcription_params_dict["sentence_level_timestamps"] else "No",
                    "Word timestamps": "Yes" if st.session_state.transcription_params_dict["word_level_timestamps"] else "No",
                    "Speaker diarization": "Yes" if st.session_state.transcription_params_dict["diarization"] else "No",
                    "Sentence diarization": "Yes" if st.session_state.transcription_params_dict["sentence_diarization"] else "No",
                    "Generate SRT": "Yes" if st.session_state.transcription_params_dict["srt"] else "No",
                    "LLM Translation": ", ".join(st.session_state.transcription_params_dict["llm_translation"]) if st.session_state.transcription_params_dict["llm_translation"] else "None",
                    "SRT Translation": ", ".join(st.session_state.transcription_params_dict["srt_translation"]) if st.session_state.transcription_params_dict["srt_translation"] else "None",
                    "Custom Vocabulary": st.session_state.transcription_params_dict["custom_vocabulary"] if st.session_state.transcription_params_dict["custom_vocabulary"] else "None",
                    "Webhook": st.session_state.transcription_params_dict["webhook"] if st.session_state.transcription_params_dict["webhook"] else "None"
                }
                
                # Display the summary
                for param, value in params_summary.items():
                    st.markdown(f"**{param}:** {value}")
            
            # Prepare parameters dictionary for API call
            transcription_params = {
                "return_as_file": st.session_state.transcription_params_dict["return_as_file"],
                "language_code": st.session_state.transcription_params_dict["language_code"],
            }
            
            # Add optional parameters only if they're set
            if st.session_state.transcription_params_dict["translate"] != "none":
                transcription_params["translate"] = st.session_state.transcription_params_dict["translate"]
                
            if st.session_state.transcription_params_dict["sentence_level_timestamps"]:
                transcription_params["sentence_level_timestamps"] = True
                
            if st.session_state.transcription_params_dict["word_level_timestamps"]:
                transcription_params["word_level_timestamps"] = True
                
            if st.session_state.transcription_params_dict["diarization"]:
                transcription_params["diarization"] = True
                
            if st.session_state.transcription_params_dict["sentence_diarization"]:
                transcription_params["sentence_diarization"] = True
                
            if st.session_state.transcription_params_dict["srt"]:
                transcription_params["srt"] = True
                
            if st.session_state.transcription_params_dict["summarize"] > 0:
                transcription_params["summarize"] = st.session_state.transcription_params_dict["summarize"]
                
            if st.session_state.transcription_params_dict["llm_translation"]:
                transcription_params["llm_translation"] = ", ".join(st.session_state.transcription_params_dict["llm_translation"])
                
            if st.session_state.transcription_params_dict["srt_translation"]:
                transcription_params["srt_translation"] = ", ".join(st.session_state.transcription_params_dict["srt_translation"])
                
            if st.session_state.transcription_params_dict["custom_vocabulary"]:
                transcription_params["custom_vocabulary"] = st.session_state.transcription_params_dict["custom_vocabulary"]
                
            # Add webhook if provided
            if st.session_state.transcription_params_dict["webhook"]:
                transcription_params["webhook"] = st.session_state.transcription_params_dict["webhook"]
                
            # Add metadata if provided
            if st.session_state.transcription_params_dict["job_metadata"]:
                try:
                    metadata_dict = json.loads(st.session_state.transcription_params_dict["job_metadata"])
                    transcription_params["metadata"] = metadata_dict
                except json.JSONDecodeError:
                    st.warning("Invalid JSON in metadata field. Using default metadata.")
            
            # Add a "Request transcription" button
            st.markdown("---")
            transcribe_button_key = f"transcribe_button_{st.session_state.filename}"
            if st.button("Request Transcription", key=transcribe_button_key, type="primary", use_container_width=True):
                # If we have a video ID, store it for later use
                if 'video_id' in st.session_state:
                    st.session_state.transcription_video_id = st.session_state.video_id
                
                on_transcription_request(signed_url, transcription_params)
                st.rerun()
        else:
            st.error(st.session_state.upload_result["message"])
    
    # Display transcription job result if available
    if st.session_state.transcription_job:
        if st.session_state.transcription_job["success"]:
            # Create a clear visual separation between job submission and transcription process
            st.markdown("---")
            st.subheader("Transcription Job Status")
            
            # Display job ID
            job_id = st.session_state.transcription_job["job_id"]
            
            # Create a status indicator
            if 'job_statuses' in st.session_state and job_id in st.session_state.job_statuses:
                job_status_info = st.session_state.job_statuses[job_id]
                current_status = job_status_info['status']
                
                # Display appropriate status message based on current status
                if current_status == 'COMPLETED':
                    st.success("✅ Transcription completed successfully!")
                    st.markdown(f"**Job ID:** {job_id}")
                elif current_status == 'FAILED':
                    st.error("❌ Transcription job failed")
                    st.markdown(f"**Job ID:** {job_id}")
                elif current_status == 'RUNNING':
                    st.info("⏳ Transcription in progress...")
                    st.markdown(f"**Job ID:** {job_id}")
                else:
                    st.info(f"ℹ️ Job status: {current_status}")
                    st.markdown(f"**Job ID:** {job_id}")
            else:
                # Initial state after submission
                st.info("⏳ Job submitted successfully. Check status to see progress.")
                st.markdown(f"**Job ID:** {job_id}")
                st.markdown("_Note: Transcription may take several minutes to complete depending on file size._")
            
            # Add buttons for job management
            col_job1, col_job2 = st.columns(2)
            
            with col_job1:
                # Add a "Check Status" button
                check_status_key = f"check_status_button_{job_id}"
                if st.button("Check Transcription Status", key=check_status_key, use_container_width=True):
                    try:
                        from backend.salad_transcribe import check_job_status
                        from dotenv import load_dotenv
                        import os
                        
                        load_dotenv()
                        salad_api_key = os.getenv("SALAD_API_KEY")
                        organization_name = os.getenv("SALAD_ORGANIZATION_NAME")
                        
                        with st.spinner(f"Checking transcription status..."):
                            # Only check status, don't create a new job
                            status = check_job_status(job_id, organization_name, salad_api_key)
                            
                            if status and "error" not in status:
                                job_status = status.get('status')
                                
                                # Store the job status and output URL in session state
                                if 'job_statuses' not in st.session_state:
                                    st.session_state.job_statuses = {}
                                
                                # Get the output URL if available
                                output_url = None
                                if 'output' in status and status['output']:
                                    output_url = status['output'].get('url')
                                
                                # Store only the necessary information
                                st.session_state.job_statuses[job_id] = {
                                    'status': job_status,
                                    'output_url': output_url
                                }
                                
                                # Display status differently based on job state
                                if job_status == 'COMPLETED' or job_status == 'succeeded':
                                    st.success("✅ Transcription completed successfully!")
                                    if output_url:
                                        st.markdown(f"**Output URL:** {output_url}")
                                elif job_status == 'FAILED' or job_status == 'failed':
                                    st.error("❌ Transcription job failed. Check details for more information.")
                                elif job_status == 'RUNNING' or job_status == 'started':
                                    st.info("⏳ Transcription is still in progress. Please check back later.")
                                elif job_status == 'PENDING' or job_status == 'pending':
                                    st.info("⏳ Transcription is queued and waiting to start. Please check back later.")
                                else:
                                    st.info(f"ℹ️ Current status: {job_status}")
                                
                                # Display job events in a more readable format
                                if 'events' in status and status['events']:
                                    with st.expander("Job Timeline"):
                                        for i, event in enumerate(status['events']):
                                            event_action = event.get('action', 'unknown')
                                            event_time = event.get('time', 'unknown time')
                                            
                                            # Format the event action for better readability
                                            if event_action == 'created':
                                                st.markdown(f"**{i+1}.** 📝 Job created at {event_time}")
                                            elif event_action == 'started':
                                                st.markdown(f"**{i+1}.** 🚀 Processing started at {event_time}")
                                            elif event_action == 'succeeded':
                                                st.markdown(f"**{i+1}.** ✅ Completed successfully at {event_time}")
                                            elif event_action == 'failed':
                                                st.markdown(f"**{i+1}.** ❌ Failed at {event_time}")
                                            else:
                                                st.markdown(f"**{i+1}.** {event_action} at {event_time}")
                                
                                # Display detailed status information
                                with st.expander("Technical Details"):
                                    st.json(status)
                                
                                # If job is completed, enable the download button
                                if job_status == 'COMPLETED' or job_status == 'succeeded':
                                    st.session_state.job_completed = True
                                
                                # Force a rerun to update the UI with the new status
                                st.rerun()
                            else:
                                error_message = status.get("error") if status else "Unknown error"
                                st.error(f"Failed to check job status: {error_message}")
                    except Exception as e:
                        st.error(f"Error checking job status: {str(e)}")
            
            with col_job2:
                # Add a direct "Download Transcription" button
                download_key = f"direct_download_button_{job_id}"
                
                # Check if we have a stored status for this job
                job_completed = False
                output_url = None
                
                if 'job_statuses' in st.session_state and job_id in st.session_state.job_statuses:
                    job_status_info = st.session_state.job_statuses[job_id]
                    job_status = job_status_info['status']
                    job_completed = job_status == 'COMPLETED' or job_status == 'succeeded'
                    output_url = job_status_info['output_url']
                
                # Change button appearance based on job status
                button_type = "primary" if job_completed else "secondary"
                
                if st.button("Download Transcription", key=download_key, use_container_width=True, type=button_type, disabled=not job_completed):
                    try:
                        from backend.salad_transcribe import check_job_status
                        from backend.test_salad_download import download_from_salad
                        from dotenv import load_dotenv
                        import os
                        
                        load_dotenv()
                        salad_api_key = os.getenv("SALAD_API_KEY")
                        organization_name = os.getenv("SALAD_ORGANIZATION_NAME")
                        
                        # If we don't have the output URL or status, check it first
                        if not job_completed or not output_url:
                            with st.spinner(f"Checking job status before download..."):
                                status = check_job_status(job_id, organization_name, salad_api_key)
                                
                                if status and "error" not in status:
                                    job_status = status.get('status')
                                    
                                    # Get output URL directly from the status response
                                    if 'output' in status and status['output']:
                                        output_url = status['output'].get('url')
                                    
                                    # Store the updated status
                                    if 'job_statuses' not in st.session_state:
                                        st.session_state.job_statuses = {}
                                    
                                    st.session_state.job_statuses[job_id] = {
                                        'status': job_status,
                                        'output_url': output_url
                                    }
                                    
                                    job_completed = (job_status == 'COMPLETED' or job_status == 'succeeded')
                                else:
                                    error_message = status.get("error") if status else "Unknown error"
                                    st.error(f"Failed to check job status: {error_message}")
                                    return
                        
                        # If job is completed and we have the URL, download it
                        if job_completed and output_url:
                            with st.spinner("Downloading transcription..."):
                                # Try to get the video ID from session state
                                video_id = None
                                
                                # First check if we have a stored video ID for this transcription
                                if 'transcription_video_id' in st.session_state:
                                    video_id = st.session_state.transcription_video_id
                                # Then try to extract from the original URL
                                elif 'original_url' in st.session_state and st.session_state.original_url:
                                    try:
                                        # Try to extract video ID using the YouTubeTranscriptDownloader
                                        downloader = YouTubeTranscriptDownloader()
                                        video_id = downloader.extract_video_id(st.session_state.original_url)
                                    except:
                                        pass
                                
                                # If we couldn't extract a video ID, use the job_id as fallback
                                filename = f"{video_id}.json" if video_id else f"{job_id}.json"
                                
                                # Download the file with the specified filename
                                output_path = download_from_salad(output_url, filename=filename)
                                
                                if output_path:
                                    st.success(f"Transcription downloaded successfully to: {output_path}")
                                    
                                    # Try to read and display a preview of the transcription
                                    try:
                                        with open(output_path, 'r', encoding='utf-8') as f:
                                            data = json.load(f)
                                            
                                            # Create a preview of the transcription
                                            if isinstance(data, dict) and 'segments' in data:
                                                segments = data['segments']
                                                if segments:
                                                    # Display first few segments
                                                    st.subheader("Transcription Preview")
                                                    for i, segment in enumerate(segments[:5]):
                                                        st.markdown(f"**{i+1}.** {segment.get('text', '')}")
                                                    
                                                    if len(segments) > 5:
                                                        st.markdown(f"*...and {len(segments)-5} more segments*")
                                            elif isinstance(data, dict) and 'text' in data:
                                                st.subheader("Transcription Preview")
                                                st.markdown(data['text'][:500] + "..." if len(data['text']) > 500 else data['text'])
                                    except Exception as e:
                                        st.warning(f"Could not display transcription preview: {str(e)}")
                                else:
                                    st.error("Failed to download transcription.")
                        elif not job_completed:
                            st.warning("Transcription is not yet complete. Please check status first.")
                        else:
                            st.error("No output URL available for download.")
                    except Exception as e:
                        st.error(f"Error downloading transcription: {str(e)}")
            
            # Add a note about the process if job is not completed
            if not ('job_statuses' in st.session_state and 
                   job_id in st.session_state.job_statuses and 
                   st.session_state.job_statuses[job_id]['status'] == 'COMPLETED'):
                st.info("ℹ️ The transcription process has two steps:")
                st.markdown("""
                1. **Job Submission** - Your request has been submitted to the transcription service
                2. **Transcription Processing** - The audio is being processed (this may take several minutes)
                
                Use the 'Check Transcription Status' button to see the current progress.
                """)
            
            # Display job details in an expander
            with st.expander("Technical Job Details"):
                st.json(st.session_state.transcription_job["details"])
        else:
            st.error(st.session_state.transcription_job["message"])
    
    # Add URL input field
    url = st.text_input(
        "YouTube URL",
        placeholder="Enter a Romanian lesson YouTube URL"
    )
    
    # Download buttons and processing
    if url:
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            if st.button("Download Transcript"):
                try:
                    downloader = YouTubeTranscriptDownloader()
                    transcript = downloader.get_transcript(url)
                    if transcript:
                        # Extract video ID and save transcript
                        video_id = downloader.extract_video_id(url)
                        if video_id and downloader.save_transcript(transcript, video_id):
                            # Store the raw transcript text in session state
                            transcript_text = "\n".join([entry['text'] for entry in transcript])
                            st.session_state.transcript = transcript_text
                            st.success(f"Transcript downloaded and saved as {video_id}.txt!")
                        else:
                            st.error("Failed to save the transcript.")
                    else:
                        st.error("No transcript found for this video.")
                except Exception as e:
                    st.error(f"Error downloading transcript: {str(e)}")
        
        with col_download2:
            # Format selection outside the button click handler
            format_option = st.radio(
                "Select format:",
                ["mp3", "original"],
                key="format_selection"
            )
            
            if st.button("Download audio"):
                success = on_download_click(url, format_option)
                if success:
                    st.success(f"Video downloaded successfully as: {st.session_state.filename}")
                    st.rerun()  # Rerun to update the UI with the download results
    
    # Show download results and upload options if download is complete
    if st.session_state.download_complete and st.session_state.video_path:
        st.subheader("Download Complete")
        st.write(f"File: {st.session_state.filename}")
        st.write(f"Path: {st.session_state.video_path}")
        
        # Upload options
        st.subheader("Upload Options")
        storage_option = st.radio(
            "Storage Service",
            ["Salad", "AWS S3", "Google Cloud"],
            index=0,  # Default to Salad
            key="storage_selection",
            label_visibility="collapsed"
        )
        
        # Use a unique key for the upload button
        upload_button_key = f"upload_button_{storage_option}_{st.session_state.filename}"
        if st.button(f"Upload to {storage_option}", key=upload_button_key):
            on_upload_click(storage_option)
            st.rerun()  # Rerun to perform the upload
    
    if st.session_state.transcript:
        st.text_area(
            label="Video transcript",
            value=st.session_state.transcript,
            height=200,
            disabled=True
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.button("Download video", use_container_width=True)
            st.button("Upload for transcribe", use_container_width=True)
            st.button("Check Status", use_container_width=True)
        with col_b:
            st.button("Save audio", use_container_width=True)
            st.button("Start transcription", use_container_width=True)
            st.button("Download subtitle", use_container_width=True)
    else:
        st.info("Please enter a YouTube URL and download the video for batch transcription.")

def render_rag_stage():
    """Render the RAG implementation stage"""
    st.header("RAG System")
    
    # Query input
    query = st.text_input(
        "Test Query",
        placeholder="Enter a question about Romanian..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retrieved Context")
        # Placeholder for retrieved contexts
        st.info("Retrieved contexts will appear here")
        
    with col2:
        st.subheader("Generated Response")
        # Placeholder for LLM response
        st.info("Generated response will appear here")

def render_structured_data_stage():
    """Render the structured data stage"""
    st.header("Structured Data")
    
    # Upload or select transcript
    st.subheader("Select Transcript Source")
    source_option = st.radio(
        "Source",
        ["Use Downloaded Transcript", "Upload Transcript File"]
    )
    
    transcript_text = None
    
    if source_option == "Use Downloaded Transcript":
        if st.session_state.transcript:
            transcript_text = st.session_state.transcript
            st.success("Using previously downloaded transcript")
        else:
            st.warning("No transcript has been downloaded yet. Please use the Raw Transcript tab first.")
    else:
        uploaded_file = st.file_uploader("Upload transcript file", type=["txt", "json"])
        if uploaded_file:
            try:
                # Check if it's JSON or plain text
                if uploaded_file.name.endswith('.json'):
                    transcript_data = json.load(uploaded_file)
                    # Handle different JSON formats
                    if isinstance(transcript_data, list) and 'text' in transcript_data[0]:
                        # YouTube transcript format
                        transcript_text = "\n".join([entry['text'] for entry in transcript_data])
                    else:
                        # Unknown format
                        st.error("Unrecognized JSON format")
                else:
                    # Plain text
                    transcript_text = uploaded_file.getvalue().decode("utf-8")
                
                st.success("Transcript loaded successfully")
            except Exception as e:
                st.error(f"Error loading transcript: {str(e)}")
    
    if transcript_text:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Raw Text")
            st.text_area(
                "Original Transcript",
                transcript_text,
                height=300,
                disabled=True
            )
        
        with col2:
            st.subheader("Structured Output")
            
            # Processing options
            process_option = st.selectbox(
                "Processing Type",
                ["Extract Dialogues", "Identify Vocabulary", "Segment by Topics"]
            )
            
            if st.button("Process Transcript"):
                with st.spinner("Processing..."):
                    # Placeholder for actual processing logic
                    if process_option == "Extract Dialogues":
                        # Simple dialogue extraction (placeholder)
                        dialogue_pattern = r'([A-Z][a-z]+):\s*(.*?)(?=\n[A-Z][a-z]+:|$)'
                        matches = re.findall(dialogue_pattern, transcript_text, re.DOTALL)
                        
                        if matches:
                            structured_data = [{"speaker": m[0], "text": m[1].strip()} for m in matches]
                            st.json(structured_data)
                        else:
                            st.info("No dialogue pattern detected. Try another processing option.")
                    
                    elif process_option == "Identify Vocabulary":
                        # Simple word frequency analysis
                        words = re.findall(r'\b[a-zA-ZăâîșțĂÂÎȘȚ]+\b', transcript_text.lower())
                        word_freq = Counter(words).most_common(20)
                        
                        st.write("Top 20 words:")
                        for word, count in word_freq:
                            st.write(f"{word}: {count}")
                    
                    else:  # Segment by Topics
                        st.info("Topic segmentation would require more advanced NLP processing.")
                        st.write("This would typically involve:")
                        st.write("1. Text embedding")
                        st.write("2. Clustering or topic modeling")
                        st.write("3. Boundary detection")

def render_interactive_stage():
    """Render the interactive learning stage"""
    st.header("Interactive Learning")
    
    # Practice type selection
    practice_type = st.selectbox(
        "Select Practice Type",
        ["Dialogue Practice", "Vocabulary Quiz", "Listening Exercise"]
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Practice Scenario")
        # Placeholder for scenario
        st.info("Practice scenario will appear here")
        
        # Placeholder for multiple choice
        options = ["Option 1", "Option 2", "Option 3", "Option 4"]
        selected = st.radio("Choose your answer:", options)
        
    with col2:
        st.subheader("Audio")
        # Placeholder for audio player
        st.info("Audio will appear here")
        
        st.subheader("Feedback")
        # Placeholder for feedback
        st.info("Feedback will appear here")

def main():
    """Main application logic"""
    render_header()
    selected_stage = render_sidebar()
    
    if selected_stage == "1. Chat with DeepSeek-R1":
        render_chat_stage()
    elif selected_stage == "2. Raw Transcript":
        render_transcript_stage()
    elif selected_stage == "3. Video to Subtitles":
        render_video_subtitles_stage()
    elif selected_stage == "4. Structured Data":
        render_structured_data_stage()
    elif selected_stage == "5. RAG Implementation":
        render_rag_stage()
    elif selected_stage == "6. Interactive Learning":
        render_interactive_stage()
    
    # Debug section at the bottom
    with st.expander("Debug Information"):
        st.json({
            "selected_stage": selected_stage,
            "transcript_loaded": st.session_state.transcript is not None,
            "chat_messages": len(st.session_state.messages)
        })

if __name__ == "__main__":
    main()