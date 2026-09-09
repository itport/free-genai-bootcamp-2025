# User Guide

## 1. Configure the application

Copy `.env.example` to `.env` and add the credentials for the services you intend to use. Start the application from the project root:

```sh
streamlit run frontend/main.py
```

## 2. Chat

Open **Chat with DeepSeek-R1** to ask questions about Romanian vocabulary, grammar, or usage. This feature requires a valid SambaNova API key.

## 3. Retrieve a transcript

Open **Raw Transcript**, paste a YouTube URL, and request its transcript. The application tries preferred Romanian and English tracks and can fall back to another available transcript. Retrieval depends on the video's settings and YouTube availability.

## 4. Process video or audio

Open **Video to Subtitles** to download media, extract audio, upload it to Salad storage, and submit a transcription job. Check the job status before downloading the result. Signed storage links can expire; do not place them in source code or commit them to Git.

FFmpeg and valid external-service credentials are required for the complete workflow.

## 5. Extract structured text

Open **Structured Data** and select a downloaded or uploaded transcript. The prototype can detect simple `Speaker: text` dialogue patterns and calculate frequent Romanian words. These are basic text-processing utilities, not semantic topic modeling.

## Limitations

This is an educational prototype. External API behavior can change, transcript access is not guaranteed, and generated language output should be reviewed by a proficient speaker.
