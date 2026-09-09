# Lang Portal

A Japanese vocabulary study portal developed from the ExamPro bootcamp starter application.

## My contribution

- completed missing Flask API endpoints for groups, words, study activities, sessions, and reviews;
- normalized the API response and route conventions;
- implemented SQLite-backed review statistics;
- connected the React/TypeScript client to the API;
- built a second, independent React frontend in `frontend-react-homebrew`.

The original course starter is available in the [ExamPro bootcamp repository](https://github.com/ExamProCo/free-genai-bootcamp-2025).

## Structure

- `backend-flask` — Flask REST API and SQLite database setup;
- `frontend-react` — React/TypeScript user interface developed against the course design;
- `frontend-react-homebrew` — independent React implementation.

## Quick start

Start the backend first:

```sh
cd backend-flask
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
invoke init-db
python app.py
```

Then start either frontend:

```sh
cd frontend-react
npm install
npm run dev
```

The API defaults to `http://localhost:5000`. For `frontend-react`, override it with the `VITE_API_BASE_URL` environment variable.
