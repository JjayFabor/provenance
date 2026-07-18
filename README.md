# Provenance

A structured peer-to-peer skill endorsement and knowledge session booking API.

Built with FastAPI, PostgreSQL, and Docker. Designed for internal teams or communities to verify skills through peer endorsements and book knowledge-sharing sessions.

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy 2.0** — ORM
- **Alembic** — database migrations
- **Docker** — containerization
- **AWS** — deployment

## Project Structure

```text
.
├── app/
│   ├── core/
│   │   ├── dependencies.py   # shared FastAPI dependencies
│   │   └── security.py       # password hashing, JWT handling
│   ├── models/               # SQLAlchemy table definitions
│   │   ├── base.py
│   │   └── user.py
│   ├── routers/              # HTTP endpoints
│   │   └── auth.py
│   ├── schemas/              # Pydantic request/response shapes
│   │   └── user.py
│   ├── config.py             # settings loaded from environment
│   ├── database.py           # engine and session setup
│   └── main.py               # FastAPI app entrypoint
├── migrations/               # Alembic migration environment
│   └── versions/
├── alembic.ini
├── requirements.txt
└── .env.example
```

## Getting Started

1. Clone the repo
2. Create and activate a virtual environment
3. Install dependencies — `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your values
5. Run migrations — `alembic upgrade head`
6. Start the server — `uvicorn app.main:app --reload`

## API Documentation

Visit `http://localhost:8000/docs` for the interactive API docs.

## Phases

- **Phase 1** — Core API: auth, skill endorsements, session booking, reputation scoring
- **Phase 2** — AI integration: skill gap analysis, smart mentor matching, session summaries