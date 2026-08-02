# Multi-Agent Research Assistant

A research assistant app with a FastAPI backend, PostgreSQL persistence, and a static HTML/CSS/JavaScript frontend. The backend coordinates multiple agent roles to generate reports, stores user accounts and report history, and exposes authenticated API routes for the browser UI.

## Features

- User registration and login with JWT authentication
- PostgreSQL database support through SQLAlchemy
- Multi-agent report generation
- Report history per user
- Report viewing, deletion, markdown download, and browser print/PDF export
- Static frontend with no Node.js build step

## Project Structure

```text
multi-agent-research/
  agents/              Agent implementations and LLM integration
  backend/             FastAPI app, auth, database, models, schemas, routes
  frontend/            Static browser frontend
  .env                 Local environment variables
  .env.example         Example environment variables
  requirements.txt     Python dependencies
```

## Requirements

- Python 3.10 or newer
- PostgreSQL database
- Groq API key
- Tavily API key

## Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/multi_agent_research
SECRET_KEY=change-this-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Use your real PostgreSQL connection string for `DATABASE_URL`.

Both of these URL formats are supported:

```env
DATABASE_URL=postgresql://user:password@host:5432/database_name
DATABASE_URL=postgres://user:password@host:5432/database_name
```

## Install Dependencies

From the project root:

```powershell
python -m pip install -r requirements.txt
```

## Run The Backend

Run this from the project root, not from inside the `backend` folder:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check that the API is running:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Run The Frontend

Open a second terminal from the project root:

```powershell
python -m http.server 5173 --directory frontend
```

Then open:

```text
http://localhost:5173
```

The frontend calls the backend at:

```text
http://localhost:8000
```

## Database Notes

The app uses SQLAlchemy models in `backend/models.py`.

On backend startup, this line in `backend/main.py` creates missing tables:

```python
Base.metadata.create_all(bind=engine)
```

The expected tables are:

- `users`
- `report_history`

If you already created tables manually, make sure their columns match the SQLAlchemy models.

## Common Issues

### `ModuleNotFoundError: No module named 'backend'`

You are probably running `uvicorn` from the wrong folder. Go to the project root first:

```powershell
cd C:\Users\dembl\OneDrive\Desktop\multi-agent-research
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### `ModuleNotFoundError: No module named 'database'`

Backend files must use package imports such as:

```python
from backend.database import Base, engine
```

The current project is configured this way.

### PostgreSQL driver error

Install dependencies again:

```powershell
python -m pip install -r requirements.txt
```

The PostgreSQL driver is included as:

```text
psycopg[binary]
```

### Frontend cannot connect

Make sure the backend is running on port `8000` before using the frontend.

## API Overview

- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /reports`
- `GET /reports`
- `GET /reports/{report_id}`
- `DELETE /reports/{report_id}`

## License

MIT
