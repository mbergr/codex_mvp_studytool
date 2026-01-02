# Guitar Practice Log

Minimal Flask app to record quick guitar practice sessions.

## Features
- Add practice entries in seconds
- View recent sessions (newest first)
- Delete entries with confirmation
- JSON API for future integrations

## Tech Stack
- Python 3.11+, Flask
- SQLAlchemy ORM (no Alembic migrations)
- SQLite by default, switchable to PostgreSQL with `DATABASE_URL`
- Server-rendered HTML with minimal CSS

## Getting Started

### Prerequisites
- Python 3.11+
- Virtual environment tool (`venv`, `pyenv`, etc.)

### Setup
1. **Clone & enter project**
   ```bash
   cd codex_mvp_studytool
   ```
2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment**
   - Copy `.env.example` to `.env` and adjust as needed.
   - By default the app uses `sqlite:///guitar_log.db` in the project root.
   - Set `DATABASE_URL` for PostgreSQL, e.g. `postgresql+psycopg2://user:pass@localhost:5432/guitar_log`.

5. **Start the app**
   ```bash
   flask --app run.py run
   ```
   The database tables are created automatically on startup. Open http://127.0.0.1:5000 to use the log.

## JSON API
- `GET /api/entries` — list entries (newest first)
- `POST /api/entries` — create an entry from JSON body `{ "duration_minutes": 20, "notes": "Pentatonic shapes" }`
- `DELETE /api/entries/<id>` — delete an entry

## Testing
Run the service-layer tests:
```bash
pytest
```

## Suggested Next Features
- Edit entry
- Tags / practice categories
- Timer mode while practicing
- Weekly totals and charts
- Search/filter
- Auth + multi-user
- Export CSV
- Sync with cloud DB
