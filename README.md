# EvalForge: The AI Trainer Arcade 🕹️

EvalForge is a **Full-Stack AI Application** that gamifies the coding feedback loop. It uses a **Judge-Coach Architecture** to provide instant grading and Socratic guidance in real-time.

## 🏗️ Architecture

The system uses a dual-agent architecture with a streaming event loop.

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI (SSE)
    participant Judge as ⚖️ Judge Agent
    participant Coach as 🧠 Coach Agent (Vertex AI)

    User->>API: POST /query/stream_v2 (Code)
    activate API
    
*   **Frontend**: React, TypeScript, Tailwind CSS, Vite
*   **Infrastructure**: Docker, Prometheus (Metrics)

## 📂 Project Structure

```
apps/web/               # React Frontend
  ├── src/components/   # Scoreboard, ChatPanel
  ├── src/hooks/        # useArcadeStream (SSE Logic)
  └── src/pages/        # DevUI (Arcade Layout)

arcade_app/             # Python Backend
  ├── agent.py          # FastAPI App & SSE Endpoint
  ├── coach_helper.py   # Socratic Coach Logic
  └── grading_helper.py # Judge Logic
```
