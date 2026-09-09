# Lang Portal API

Flask and SQLite backend for the Lang Portal vocabulary application.

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
invoke init-db
python app.py
```

The server listens on port `5000`. `invoke init-db` creates `words.db`, applies the SQL files under `sql/setup`, and imports the JSON seed data under `seed`.

To recreate the local database, delete `words.db` and run `invoke init-db` again. The database is generated locally and is excluded from version control.

## API areas

- dashboard statistics and recent sessions;
- vocabulary words and groups;
- study activities;
- study-session creation and history;
- per-word review results and aggregate counts.
