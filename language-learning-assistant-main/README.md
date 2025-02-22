# Language Learning Assistant

## Project Evolution

This project was developed based on the skeleton provided by labeveryday, which initially consisted of only the frontend implementation. Through several iterations and improvements, we've enhanced its capabilities and performance.

## Key Technical Changes

### LLM Model Transition
- Migrated from Amazon's NOVA to DeepSeek-R1
- Enhanced response quality and processing capabilities
- Improved language understanding and generation

### Frontend Enhancements
- Implemented streaming responses in Streamlit
- Provides real-time feedback and more engaging user experience
- Smoother interaction with the language learning process

### YouTube Transcript Integration
- Initially tested Google's YouTube API for subtitle access
  - Found limitations in terms of quota and accessibility
- Successfully implemented youtube-transcript-api
  - More reliable and efficient transcript retrieval
  - No API quota limitations
  - Better support for multiple languages

## Technical Stack

- **Frontend**: Streamlit
- **LLM**: DeepSeek-R1
- **Transcript API**: youtube-transcript-api
- **Data Storage**: SQLite (for vector storage)

## Features

- Interactive language learning experience
- Real-time streaming responses
- Efficient transcript processing
- RAG (Retrieval Augmented Generation) implementation
- Structured learning approach

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run the application: `streamlit run frontend/main.py`

## License

See the [LICENSE](LICENSE) file for details.