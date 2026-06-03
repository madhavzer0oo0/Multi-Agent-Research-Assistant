# Multi-Agent Research

Lightweight research platform that coordinates multiple agent roles (researcher, critic, writer, summarizer, and a coordinator) with a FastAPI backend and a minimal frontend.

**Quick summary:** orchestrates agent interactions, persists reports via the backend, and exposes a simple frontend for viewing and interacting with the system.

**Requirements:**
- **Python:** 3.10+
- **Packages:** see `requirements.txt` (install with `pip install -r requirements.txt`)

**Project layout**
- **`agents/`**: agent implementations and `llm.py` interface (see [agents/coordinator_agent.py](agents/coordinator_agent.py), [agents/research_agent.py](agents/research_agent.py)).
- **`backend/`**: FastAPI app, DB layer, auth and API routes (entry: [backend/main.py](backend/main.py)).
- **`frontend/`**: small UI and pages (entry: [frontend/app.py](frontend/app.py)).
- Top-level: `app.py` (frontend runner), `requirements.txt`, ReadME.md.

**Quick start (development)**
1. Create and activate a virtualenv (recommended):

```
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set environment variables (example):

- `DATABASE_URL` — database connection string (if applicable)
- `SECRET_KEY` — app secret for auth
- `OPENAI_API_KEY` — optional: LLM API key used by `agents/llm.py`

4. Run the backend API:

```
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

5. Run the frontend (from project root):

```
python app.py
```

If the frontend uses Streamlit, you can run:

```
cd frontend
streamlit run app.py
```

**Agents (overview)**
- **Coordinator** (`agents/coordinator_agent.py`): orchestrates tasks across agents and composes workflows.
- **Researcher** (`agents/research_agent.py`): performs information gathering and research steps.
- **Critic** (`agents/critic_agent.py`): evaluates outputs and suggests improvements.
- **Writer** (`agents/writer_agent.py`): drafts text and generates report content.
- **Summarizer** (`agents/summerizer_agent.py`): condenses results into concise summaries.
- **LLM interface** (`agents/llm.py`): single place to integrate with external LLM providers.

**Backend notes**
- API routes are under `backend/routes/` (see [backend/routes/report_routes.py](backend/routes/report_routes.py) and [backend/routes/auth_routes.py](backend/routes/auth_routes.py)).
- DB models and schemas live in `backend/models.py` and `backend/schemas.py`.

**Development tips**
- Keep secrets out of version control; use a `.env` file or your OS environment.
- If you add new dependencies, update `requirements.txt` with `pip freeze > requirements.txt` from your virtualenv.

**Contributing**
- Open issues for bugs or enhancements.
- Create feature branches and submit PRs with clear descriptions and tests where applicable.

**License**
- MIT (or change to your preferred license).

If you want, I can also:
- add a `.env.example` with recommended variables
- add a `Makefile` or `scripts/` to simplify common commands
- run the app locally and verify endpoints
