# Romanian Learning Assistant

An educational Streamlit prototype that combines Romanian-language LLM interaction with YouTube transcript and media-processing workflows.

## Implemented capabilities

- Romanian-language chat using DeepSeek-R1 through the SambaNova API;
- YouTube transcript retrieval with Romanian/English fallback;
- video download and audio extraction;
- object-storage upload and Salad transcription job submission/status checks;
- optional timestamps, diarization, summaries, translations, and SRT output supported by the transcription service;
- basic dialogue extraction and Romanian vocabulary-frequency analysis.

This prototype does **not** implement retrieval-augmented generation, vector storage, or an autonomous learning agent.

## Setup

Requirements include Python, FFmpeg, and credentials for the external services you choose to use.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run frontend/main.py
```

Populate `.env` with your own credentials. Never commit the populated file.

## Main components

- `backend/chat.py` — streamed SambaNova chat integration;
- `backend/improved_transcript_downloader.py` — transcript discovery and fallback;
- `backend/video_downloader.py` — media download and audio extraction;
- `backend/salad_transcribe.py` — transcription job submission and status handling;
- `frontend/main.py` — Streamlit workflow and structured-text tools.

See the [user guide](docs/user_guide.md) and [transcript fallback note](docs/direct_translation_issue.md) for additional context.

## Status and limitations

The application is a course prototype and depends on third-party APIs whose contracts and availability may change. It should not be treated as a production service without stronger validation, automated tests, access control, and deployment hardening.

## License

[MIT](LICENSE)
