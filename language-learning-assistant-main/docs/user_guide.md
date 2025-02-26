# Romanian Learning Assistant - User Guide

## Overview

The Romanian Learning Assistant is a comprehensive tool designed to help you learn Romanian through YouTube videos. It provides several features:

1. **Chat with DeepSeek-R1**: Interact with an AI assistant to ask questions about Romanian language
2. **Raw Transcript**: Download and analyze transcripts from YouTube videos
3. **Video to Subtitles**: Download videos, process them, and generate high-quality transcriptions
4. **Structured Data**: Extract dialogues and vocabulary from transcripts
5. **RAG Implementation**: Ask questions about specific Romanian content
6. **Interactive Learning**: Practice Romanian through interactive exercises

## Getting Started

### Navigation

The application is organized into different stages, accessible from the sidebar:

- Use the sidebar to navigate between different stages of the application
- Each stage focuses on a specific aspect of language learning
- The current stage is highlighted in the sidebar

## Stage 1: Chat with DeepSeek-R1

This stage allows you to interact with an AI assistant specialized in Romanian language.

1. Type your question in the chat input at the bottom of the screen
2. The AI will respond with information about Romanian grammar, vocabulary, or cultural aspects
3. Example questions are provided in the sidebar for quick access
4. Your conversation history is maintained throughout your session
5. Use the "Clear Chat" button to start a new conversation

## Stage 2: Raw Transcript Processing

This stage helps you download and analyze transcripts from YouTube videos.

1. Enter a YouTube URL in the input field
2. Click "Download Transcript" to retrieve the transcript
3. The transcript will be displayed in the "Raw Transcript" section
4. Statistics about the transcript (character count, line count) are shown in the "Transcript Stats" section
5. Transcripts are saved to the "transcripts" folder with the video ID as the filename

## Stage 3: Video to Subtitles

This is the main workflow for processing videos and generating high-quality transcriptions:

### Step 1: Download Video
1. Enter a YouTube URL in the input field
2. Select the format (mp3 or original)
3. Click "Download audio" to retrieve the audio/video
4. The system will extract the video ID and download the content
5. Once complete, you'll see "Download Complete" with file details

### Step 2: Upload to Cloud Storage
1. After downloading, select a storage service (Salad, AWS S3, Google Cloud)
2. Click "Upload to [selected service]"
3. The system will upload your file to the selected storage service
4. Once complete, you'll see a success message and a signed URL

### Step 3: Configure Transcription Parameters
After uploading, you can configure transcription parameters across three pages:

**Page 1: Basic Parameters**
- Language Code: Select the primary language of the video
- Translation: Choose whether to translate the transcript
- Return as file: Get the transcript as a downloadable file
- Summarize: Generate a summary of specified length

**Page 2: Timestamp & Diarization Options**
- Sentence-level timestamps: Add timestamps for each sentence
- Word-level timestamps: Add timestamps for each word
- Generate SRT: Create subtitle file in SRT format
- Speaker diarization: Identify different speakers
- Sentence diarization: Group sentences by speaker

**Page 3: Advanced Options**
- LLM Translation Languages: Select languages for AI translation
- SRT Translation Languages: Select languages for subtitle translation
- Custom Vocabulary: Add specialized terms to improve accuracy
- Webhook URL: Receive notifications when processing completes
- Job Metadata: Add custom metadata to the job

### Step 4: Request Transcription
1. Review your selected parameters in the "View Selected Parameters" section
2. Click "Request Transcription" to submit the job
3. The system will send your request to the transcription service
4. You'll see "Transcription job submitted successfully!" when the request is accepted

### Step 5: Monitor Transcription Progress
1. After submission, you'll see the "Transcription Job Status" section
2. The job starts in "pending" or "running" state
3. Click "Check Transcription Status" to update the status
4. The "Job Timeline" shows the progression of events
5. Technical details are available in the expandable sections

### Step 6: Download Transcription
1. Once the job status shows "completed" or "succeeded", the "Download Transcription" button becomes active
2. Click "Download Transcription" to retrieve the result
3. The file is saved with the video ID as the filename (e.g., "5eXEeG-V_mo.json")
4. A preview of the transcription is displayed after download
5. The full transcription is available in the saved file

## Stage 4: Structured Data

This stage helps you extract structured information from transcripts:

1. Select a transcript source (previously downloaded or upload a new file)
2. Choose a processing type:
   - Extract Dialogues: Identify speakers and their lines
   - Identify Vocabulary: Find the most common words
   - Segment by Topics: Group content by subject matter
3. Click "Process Transcript" to analyze the content
4. View the structured output in the right column

## Stage 5: RAG Implementation

This stage allows you to ask questions about specific Romanian content:

1. Enter a question in the "Test Query" field
2. The system retrieves relevant context from the available transcripts
3. An AI-generated response is provided based on the retrieved context

## Stage 6: Interactive Learning

This stage offers interactive exercises to practice Romanian:

1. Select a practice type (Dialogue, Vocabulary, Listening)
2. Interact with the practice scenario
3. Select answers from the provided options
4. Receive feedback on your responses

## Troubleshooting

- If a transcript download fails, try a different video or check if the video has captions
- If video download fails, ensure the video is publicly available and not restricted
- If transcription fails, check your parameters and try again
- Use the "Debug Information" section at the bottom to see the current state of the application

## Tips for Best Results

1. Use videos with clear audio for better transcription quality
2. Romanian videos with existing subtitles work best for transcript download
3. Shorter videos (under 10 minutes) process faster
4. MP3 format is recommended for transcription-only purposes
5. Check transcription status periodically as processing can take several minutes
6. Save important transcriptions to your local device as cloud storage links may expire