import asyncio
from arcade_app.database import get_session
from arcade_app.models import Project, KnowledgeChunk
from sqlmodel import select
from datetime import datetime

async def main():
    print("Seeding projects...")
    user_id = "leo"
    repo_url = "https://github.com/leok974/ApplyLens"
    
    async for session in get_session():
        # 1. Check if exists
        result = await session.execute(select(Project).where(Project.repo_url == repo_url))
        existing = result.scalar_one_or_none()
        
        if not existing:
            print(f"Creating project {repo_url}...")
            proj = Project(
                owner_user_id=user_id,
                name="ApplyLens",
                repo_url=repo_url,
                default_world_id="world-python",
                sync_status="ok",
                last_sync_at=datetime.utcnow(),
                summary_data={"stack": ["fastapi", "react"], "primary_language": "python"}
            )
            session.add(proj)
            await session.commit()
            await session.refresh(proj)
            print(f"Created project ID: {proj.id}")
            existing = proj

        # 2. Seed/Update Codex Entries (Overview, Architecture, Quest Hooks)
        print("Seeding/Updating project codex docs...")
        
        # Define the three doc types with full content
        codex_docs = [
            {
                "chunk_index": 0,
                "title": "ApplyLens: Overview",
                "content": """---
project: applylens
doc_type: overview
worlds: [world-python, world-sql, world-infra, world-agents]
level: 2
stack:
  frontend: React + Vite + Tailwind (dark-first)
  backend: FastAPI (Python)
  storage:
    - PostgreSQL
    - Elasticsearch
    - Redis
  infra:
    - Docker Compose
    - Cloudflare Tunnel
    - GitHub Actions
domains:
  - job_search
  - email_processing
  - productivity
primary_languages:
  - python
  - typescript
status: active
---

# ApplyLens

## Mission

ApplyLens is an AI-powered job search companion that lives in your inbox.
It ingests emails from Gmail, organizes opportunities into an application
tracker, and uses search + agents to help you stay on top of your job hunt.

## Core Features

- **Inbox ingest:** Pulls relevant job-related threads from Gmail into a local store.
- **Powerful search:** Elasticsearch-backed search across subject, body, labels, and metadata.
- **Application tracker:** Tracks each application with status, company, role, and dates.
- **Reply analytics:** Computes time-to-reply metrics and reply counts per thread.
- **Companion agent (extension):** Browser extension that helps fill forms and write outreach messages.

## Tech Stack (High Level)

- **Frontend:** React + Vite + Tailwind, dark theme, shadcn-like components, Playwright e2e.
- **Backend:** FastAPI, pydantic models, Alembic migrations.
- **Storage:**
  - PostgreSQL for primary data (emails, threads, applications, metrics).
  - Elasticsearch for full-text search and suggestions.
  - Redis for caching and background job coordination (where used).
- **Infra:** Docker Compose for dev/prod, Cloudflare Tunnel for public routing, GitHub Actions for CI/CD.
- **AI / ML:**
  - LLMs for classification, suggestions, and text generation (agents and companion).
  - ES analyzers tuned for job-related language.

## Worlds & Skills (EvalForge Mapping)

- **Python / Backend (The Foundry):**
  - Models, ingest pipelines, FastAPI endpoints, db migrations.
- **SQL / Data (The Archives):**
  - Schema design for `emails`, `applications`, `metrics`.
  - Queries for analytics and dashboards.
- **Infra / DevOps (The Grid):**
  - Compose stack, tunnels, health checks, resource limits.
- **Agents (The Oracle):**
  - Inbox triage agent, companion tools, bandit-style learning loops.
- **Git / Process (The Timeline):**
  - Feature branches, migrations, and deployment workflows.

## Current Maturity

- Stage: **active prototype / early production**.
- Test coverage: API + e2e coverage for key flows (search, ingest, tracker).
- Observability: Basic health endpoints and dashboards; more agent metrics planned.
"""
            },
            {
                "chunk_index": 1,
                "title": "ApplyLens: Architecture",
                "content": """---
project: applylens
doc_type: architecture
worlds: [world-python, world-sql, world-infra, world-agents]
level: 3
stack:
  frontend: React + Vite + Tailwind
  backend: FastAPI
  storage:
    - PostgreSQL
    - Elasticsearch
    - Redis
key_services:
  - name: web
    type: frontend
  - name: api
    type: backend
  - name: es
    type: search
  - name: db
    type: database
  - name: redis
    type: cache
---

# ApplyLens Architecture

## High-Level Components

- **Web App (`apps/web`):**
  - React + Vite SPA.
  - Routes for Inbox, Search, Tracker, Settings, and Companion.
  - Talks to the API via `/api/...` endpoints.

- **API (`services/api` or `services/backend`):**
  - FastAPI application exposing REST endpoints for:
    - `/emails` and `/threads`
    - `/search` (ES-backed)
    - `/applications`
    - `/metrics` and health checks
    - `/extension/...` for the browser companion

- **PostgreSQL (DB):**
  - Stores normalized email threads, application records, reply metrics, and agent logs.

- **Elasticsearch (Search):**
  - Indexes email subjects, bodies, and derived fields.
  - Provides BM25 search, autocomplete, and label-aware scoring.

- **Redis (Optional but recommended):**
  - Used for caching and background tasks when enabled.

## Core Data Flow: Inbox → Tracker

1. **Gmail ingest:**
   - A backfill or scheduled job pulls messages from Gmail using OAuth.
   - Raw Gmail threads are normalized into internal `EmailThread` and `EmailMessage` models.

2. **Normalization & Enrichment:**
   - The backend classifies messages (offer, interview, rejection, promo, etc.).
   - It computes reply metrics (`first_user_reply_at`, `replied`, counts) and label hints.

3. **Storage:**
   - Normalized entities are stored in PostgreSQL.
   - A search document per thread is written to Elasticsearch with shingled fields and analyzers.

4. **Search & Tracker:**
   - The web app calls `/api/search` for inbox/search views with filters and sort.
   - The tracker calls `/api/applications` to render application rows and status chips.

5. **Companion & Agents:**
   - The companion extension calls dedicated endpoints to:
     - Generate form answers or outreach messages.
     - Log applications and user actions.
   - Future agents consume the same API surface.

## Key Modules / Folders (Example)

- `apps/web/src/features/inbox` – inbox UI and search components.
- `apps/web/src/features/tracker` – application tracker grid and filters.
- `services/api/app/models` – pydantic and ORM models.
- `services/api/app/routes` – FastAPI route handlers.
- `services/api/app/search` – ES query builders and analyzers.
- `infra/` – docker-compose files, nginx/tunnel configs (in infra repo if separate).

## Important Invariants

- Threads are the primary unit of conversation; metrics and search docs are thread-based.
- Applications reference a *canonical* thread and keep status in Postgres (Single Source of Truth).
- Search must never leak emails for other users/tenants (if multi-user is enabled).

## Scaling & Performance Notes

- Heavy work (ingest + indexing) should happen in background jobs where possible.
- Elasticsearch queries can be tuned via:
  - Label boosts (offers > interviews > rejections).
  - Recency decay on received time.
- Bottlenecks to watch:
  - Long-running Gmail ingest jobs.
  - Overly expensive ES queries (deep pagination, wildcards).
"""
            },
            {
                "chunk_index": 2,
                "title": "ApplyLens: Quest Hooks",
                "content": """---
project: applylens
doc_type: quest_hooks
worlds: [world-python, world-sql, world-infra, world-agents]
level: 2
quest_ideas:
  - id: "applylens-search-filter-job-type"
    world: world-python
    description: "Add a job-type filter (full-time / internship / contract) to /api/search and wire it to the web UI."
  - id: "applylens-es-score-tuning"
    world: world-sql
    description: "Tune Elasticsearch scoring so offers and interviews rank above generic newsletters."
  - id: "applylens-agent-autofill"
    world: world-agents
    description: "Extend the Companion agent to learn from past edits and improve autofill quality."
boss_ideas:
  - id: "applylens-inbox-boss"
    world: world-agents
    description: "Design an Inbox Triage Boss that classifies new emails and proposes safe follow-up actions with clear logs and rollbacks."
---

# Quest Hooks – ApplyLens

## Good Practice Quests

1. **Job Type Filter for Search (Backend + Frontend)**  
   Add a `job_type` filter to the search API and UI. Make sure it's indexed in ES and properly validated.

2. **Ranking for High-Value Threads (Search Tuning)**  
   Adjust ES boosts so offers and interviews reliably show up at the top of the results.

3. **Smarter Autofill (Companion Learning Loop)**  
   Log user edits to generated answers and feed them back into the suggestion style.

## Boss Fights

1. **Inbox Triage Boss**  
   Build or extend an agent that:
   - Monitors new threads ingested from Gmail.
   - Classifies them into categories (offer, interview, lead, spam).
   - Suggests safe next actions (reply, ignore, archive) with human approval.
   - Logs every decision for audit and rollback.
"""
            }
        ]
        
        # Get all existing chunks for this project
        stmt = select(KnowledgeChunk).where(
            KnowledgeChunk.source_id == existing.id,
            KnowledgeChunk.source_type == "project"
        )
        result = await session.execute(stmt)
        existing_chunks = {chunk.chunk_index: chunk for chunk in result.scalars().all()}
        
        # Create or update each doc
        for doc in codex_docs:
            idx = doc["chunk_index"]
            if idx in existing_chunks:
                print(f"Updating chunk {idx}: {doc['title']}")
                existing_chunks[idx].content = doc["content"]
                session.add(existing_chunks[idx])
            else:
                print(f"Creating chunk {idx}: {doc['title']}")
                chunk = KnowledgeChunk(
                    source_type="project",
                    source_id=existing.id,
                    chunk_index=idx,
                    content=doc["content"],
                    embedding=[0.0]*768  # Mock embedding
                )
                session.add(chunk)
            
        await session.commit()
        print(f"✅ Successfully seeded {len(codex_docs)} Codex docs for ApplyLens")

if __name__ == "__main__":
    asyncio.run(main())
