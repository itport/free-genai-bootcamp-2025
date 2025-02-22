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
from backend.get_transcript import YouTubeTranscriptDownloader
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
            if st.button("Download Video"):
                try:
                    video_downloader = YouTubeVideoDownloader()
                    video_path = video_downloader.download_video(url)
                    if video_path:
                        st.success(f"Video downloaded successfully to {video_path}!")
                    else:
                        st.error("Failed to download the video.")
                except Exception as e:
                    st.error(f"Error downloading video: {str(e)}")

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
            if st.button("Download Video"):
                try:
                    with st.spinner("Downloading and processing video..."):
                        video_downloader = YouTubeVideoDownloader()
                        # First extract video info to show progress
                        video_id = video_downloader.extract_video_id(url)
                        if not video_id:
                            st.error("Invalid YouTube URL or unable to extract video ID")
                            return
                            
                        st.info(f"Processing video ID: {video_id}")
                        video_path = video_downloader.download_video(url)
                        
                        if video_path:
                            # Convert to absolute path if needed
                            if not os.path.isabs(video_path):
                                video_path = os.path.abspath(video_path)
                            st.success("Video downloaded and converted to audio successfully!")
                            st.session_state.audio_path = video_path
                        else:
                            # Display the specific error message from the backend
                            st.error("Failed to download and process the video. Please check the following possible issues:\n" +
                                    "1. Video availability and accessibility\n" +
                                    "2. Audio format availability\n" +
                                    "3. Disk space and permissions\n" +
                                    "4. FFmpeg installation for audio conversion")
                except Exception as e:
                    st.error(f"Error downloading video: {str(e)}")
    
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