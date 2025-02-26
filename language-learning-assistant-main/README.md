# Romanian Learning Assistant

A comprehensive tool for learning Romanian through YouTube videos, featuring transcript processing, AI-powered chat, and interactive learning.

## Features

- **AI-Powered Language Assistant**: Chat with DeepSeek-R1 for Romanian language assistance
- **YouTube Integration**: Download videos, audio, and transcripts directly from YouTube URLs
- **Advanced Transcription**:
  - Multi-language support (Romanian, English, and other languages)
  - Speaker diarization (identify different speakers)
  - Word and sentence-level timestamps
  - Automatic summarization
  - SRT subtitle generation
- **Multi-language Translation**:
  - Translate transcripts to English
  - Generate translations in multiple languages (German, Italian, French, Spanish, etc.)
- **Structured Data Extraction**:
  - Extract dialogues with speaker identification
  - Vocabulary frequency analysis
  - Topic segmentation
- **Cloud Storage Integration**:
  - Upload to Salad storage
  - Support for AWS S3 and Google Cloud (coming soon)
- **Streaming Response**: Real-time streaming of AI responses for a more interactive experience
- **Batch Processing**: Process multiple videos in sequence
- **Interactive Learning**: Practice Romanian through guided exercises
- **RAG Implementation**: Ask questions about specific Romanian content with context retrieval

## GitHub Upload Guide

When uploading this project to GitHub, make sure to include the following directories and files:

### Include These:

- `frontend/` - Contains the Streamlit UI code
- `backend/` - Contains the core functionality modules
- `docs/` - Contains documentation including the user guide
- `.gitignore` - Prevents sensitive and unnecessary files from being uploaded
- `requirements.txt` - Lists all Python dependencies
- `README.md` - Project documentation (this file)

### Exclude These (already in .gitignore):

- `videos/` - Contains downloaded videos
- `transcripts/` - Contains downloaded transcripts
- `audio/` - Contains extracted audio
- Any `.env` files or files containing API keys
- Any downloaded media files (mp3, mp4, etc.)
- Any generated transcription files
- Virtual environment directories (venv, env)
- IDE configuration files (.vscode, .idea)
- `__pycache__/` directories and `.pyc` files

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API keys:
   ```
   SALAD_API_KEY=your_salad_api_key
   SALAD_ORGANIZATION_NAME=your_organization_name
   ```
6. Run the application: `streamlit run frontend/main.py`

## Usage

See the [User Guide](docs/user_guide.md) for detailed instructions on how to use the application.

## Key Components

- **YouTubeTranscriptDownloader**: Downloads and processes transcripts from YouTube videos
- **ImprovedTranscriptDownloader**: Enhanced version with better language detection and fallback options
- **YouTubeVideoDownloader**: Downloads videos and extracts audio in various formats
- **SambanovaChat**: Provides the AI chat interface with streaming responses
- **Structured Data Processing**: Extracts dialogues, vocabulary, and topics from transcripts

## Technical Features

- **Session State Management**: Persistent state across user interactions
- **Responsive UI**: Adapts to different screen sizes with column layouts
- **Error Handling**: Comprehensive error handling for API calls and file operations
- **Progress Indicators**: Spinners and status messages for long-running operations
- **Modular Design**: Separate modules for different functionality
- **Streaming Responses**: Real-time text generation for chat interactions
- **Paginated Parameter Configuration**: Book-like navigation for complex settings

## License

[MIT License](LICENSE)

## Acknowledgements

- DeepSeek-R1 for language model capabilities
- Streamlit for the web interface
- YouTube Transcript API for transcript retrieval
- Salad API for transcription services