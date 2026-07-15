# HasMyIdeaBeenTaken

A production-ready Python template for a semantic search system that indexes open-source repositories and compares user ideas against existing projects.

## Overview

HasMyIdeaBeenTaken is inspired by HaveIBeenPwned, but for software ideas and repositories. The core flow is:

1. A background scraper ingests repository metadata and descriptions.
2. An AI layer generates meaningful summaries for each repository.
3. Users submit a natural-language idea prompt.
4. A semantic/hybrid search service ranks existing repositories by similarity and returns a comparison table.

This repository is a clean, portfolio-friendly starter with layered architecture, typed models, and database-backed search primitives.

## Architecture

```text
Client
  |
  v
FastAPI Web API
  |   \
  |   +--> SearchService
  |   +--> RepositoryRepository
  |
  +--> SQLAlchemy ORM
         |
         v
      SQLite (MVP) / PostgreSQL-ready

Background Worker / Scraper
  |
  +--> RepositoryRepository
  +--> AI Summary Generation
```

## Directory Structure

```text
HasMyIdeaBeenTaken/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   └── search.py
│   │   └── main.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project_context.py
│   │   ├── repository.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── base.py
│   │   └── repository_repository.py
│   ├── schemas/
│   │   └── repository.py
│   └── services/
│       ├── scraper_service.py
│       └── search_service.py
├── scripts/
│   └── seed_demo.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Database Schema

The normalized MVP schema is composed of:

- `owners`: platform owner metadata
- `repositories`: repository inventory and lookup data
- `project_context`: AI-generated summary and contextual metadata

### SQLAlchemy Model Summary

```python
class Owner(Base):
    __tablename__ = "owners"
    id: int
    platform_username: str
    platform_profile_url: str | None

class Repository(Base):
    __tablename__ = "repositories"
    id: int
    owner_id: int
    repository_name: str
    source_platform: str
    repository_url: str
    created_at: datetime
    updated_at: datetime

class ProjectContext(Base):
    __tablename__ = "project_context"
    id: int
    repository_id: int
    raw_description: str | None
    ai_generated_summary: str | None
    embedding_vector: str | None
```

## Core Components

### 1. Repository Pattern

The app uses a `BaseRepository` abstraction and a `RepositoryRepository` specialization to encapsulate persistence operations.

### 2. Search Service

The `SearchService` performs a normalized keyword search across repository names, owner names, and AI summaries. In production, this can be upgraded to vector similarity with `pgvector` or a dedicated embedding service.

### 3. Scraper Worker

The `ScraperService` ingests repository seed data and stores the metadata in a clean transaction flow.

## Local Setup

### Option A: Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn app.api.main:app --reload
```

### Option B: Docker

A Docker example can be added later for production parity, but the current MVP is intentionally lightweight and easy to run.

## API Endpoints

### Health

- `GET /health`

### Search

- `POST /api/search`

Example payload:

```json
{
  "repository_name": "hello-world",
  "owner_username": "octocat",
  "owner_profile_url": "https://github.com/octocat",
  "repository_url": "https://github.com/octocat/hello-world",
  "source_platform": "github",
  "raw_description": "A simple demo repository",
  "ai_generated_summary": "A beginner-friendly example repository",
  "embedding_vector": "demo-embedding-vector"
}
```

## Semantic Search Strategy

The MVP uses a dependency-free keyword search and is structured to evolve into embedding-based similarity search:

1. Generate embeddings for each repository summary.
2. Store embeddings in a vector-capable database.
3. Query nearest neighbors using an ANN search strategy.
4. Rank matches with metadata and confidence scoring.

For production, PostgreSQL with `pgvector` is recommended.

## Recommended Next Steps

- Add Pydantic response schemas
- Add async background worker using Celery or RQ
- Add OpenAI/Ollama integration for summaries and embeddings
- Switch from SQLite to PostgreSQL with `pgvector`
- Add authentication and rate limiting
- Add Docker Compose and CI checks

## Conclusion

This starter gives you a strong, maintainable foundation for building a portfolio-grade semantic search product. It demonstrates clean module boundaries, domain modeling, and API-first backend architecture.
