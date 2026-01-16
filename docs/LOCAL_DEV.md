# 🚀 EvalForge Local Development Guide

This guide gets you from zero to fully running local dev environment in **under 5 minutes**.

---

## ⚡ Quick Start (The Fast Path)

### Option 1: One-Command Start (Recommended)

```powershell
# 1. Start everything (Deps + API + Web) in one go
pnpm dev:all
```

*Note: Requires `pnpm` installed.*

### Option 2: Component Control

```powershell
# 1. Start Infrastructure (Postgres + Redis)
# Uses docker-compose.dev.yml automatically
pnpm dev:deps

# 2. Start Services (separate terminals)
pnpm dev:api   # Backend
pnpm dev:web   # Frontend
```

### First Time Setup
```powershell
pnpm dev:init-db  # Create schema
pnpm dev:seed     # Seed data
```

Then open: **http://localhost:5173/arcade/workshop**

✨ **That's it!** You now have:
- Local Postgres (port 5435) via Docker Compose
- Local Redis (port 6379) via Docker Compose
- Backend API (port 8092) with hot-reload
- Frontend (port 5173) with HMR

---

## 📦 Available Scripts

| Command | Description |
|---------|-------------|
| `pnpm dev:all` | **Start EVERYTHING** (Deps, API, Web) concurrently |
| `pnpm dev:deps` | Start Docker services (Postgres, Redis) via Compose |
| `pnpm dev:init-db` | Initialize database schema |
| `pnpm dev:seed` | Seed universe data (worlds, tracks, quests) |
| `pnpm dev:api` | Start backend server (port 8092) |
| `pnpm dev:web` | Start frontend dev server (port 5173) |

---

## 🔧 Configuration

### Environment Variables

The system auto-configures based on environment:

**Development (local, outside Docker):**
- Database: `127.0.0.1:5435`
- Redis: `127.0.0.1:6379`

**Docker (inside containers):**
- Database: `db:5432`
- Redis: `redis:6379`

**Override anything** by setting env vars:
```powershell
$env:DATABASE_URL = "postgresql+asyncpg://user:pass@host:port/dbname"
$env:REDIS_URL = "redis://host:port/0"
```

### Auto-Init Database

By default, the backend does **not** auto-init the database on startup. You control this via:

```powershell
# Enable auto-init (runs init_db on startup)
$env:AUTO_INIT_DB = "1"

# Disable auto-init (default)
$env:AUTO_INIT_DB = "0"
```

When enabled, the backend will automatically create schema if it doesn't exist (with 30s timeout protection).

---

## 🧪 Smoke Test Your Setup

After starting, verify everything works:

### 1. Backend Health
```powershell
curl http://127.0.0.1:8092/health
# Expected: {"status":"ok","version":"0.4.0"}
```

### 2. Universe Data
```powershell
curl http://127.0.0.1:8092/api/universe
# Expected: JSON with worlds array (Python, TypeScript, Java)
```

### 3. Quest Data
```powershell
curl "http://127.0.0.1:8092/api/quests/?world_id=world-python"
# Expected: JSON array with Python quests
```

### 4. Frontend
Open http://localhost:5173/arcade/workshop

Console should show:
```
[useAuth] DEV mode (localhost) – using fake user, no /api/auth/me call
```

UI should display:
- World dropdown: "The Foundry", "The Prism", "The Reactor"
- Track dropdown (populated based on selected world)
- Starter quest available

---

## 🐛 Troubleshooting

### "Database connection failed"

**Check if PostgreSQL is running:**
```powershell
docker ps | Select-String "evalforge-db"
```

**Restart it:**
```powershell
pnpm dev:deps
```

### "RemoteProtocolError" during API tests
This usually happens when `uvicorn` reloads mid-request due to code changes.
**Fix:** Run the server in **stable mode** (no reload) for automated verification:
```powershell
python -m uvicorn arcade_app.agent:app --host 127.0.0.1 --port 8092
```

### "Redis connection failed"

**Check if Redis is running:**
```powershell
docker ps | Select-String "evalforge-redis"
```

**Restart it:**
```powershell
docker stop evalforge-redis
docker rm evalforge-redis
pnpm dev:deps
```

### "WebSocket /ws/game_events errors"

This is **normal** if Redis isn't running. HTTP API routes work fine without it.

To enable WebSocket (for real-time events):
```powershell
pnpm dev:deps  # Ensures Redis is running
```

### "init_db hangs"

If you manually run `init_db` and it hangs, **the schema probably already exists**. This is safe to ignore.

**Clean slate approach:**
```powershell
# 1. Drop the database
docker exec -it evalforge-db psql -U evalforge_app -d postgres -c "DROP DATABASE evalforge;"

# 2. Recreate it
docker exec -it evalforge-db psql -U evalforge_app -d postgres -c "CREATE DATABASE evalforge OWNER evalforge_app;"

# 3. Re-init
pnpm dev:init-db
pnpm dev:seed
```

### "Frontend shows blank screen"

**Check backend is running:**
```powershell
curl http://127.0.0.1:8092/health
```

**Check Vite dev server:**
```powershell
curl http://localhost:5173/
```

**Check browser console** for errors.

---

## 📂 Key Files

### Configuration
- [`arcade_app/config.py`](arcade_app/config.py) - Centralized config (DB, Redis, auto-init)
- [`apps/web/.env.local`](apps/web/.env.local) - Frontend dev config
- [`apps/web/vite.config.ts`](apps/web/vite.config.ts) - Vite proxy to backend

### Scripts
- [`scripts/dev-deps.ps1`](scripts/dev-deps.ps1) - Check/start Docker services
- [`scripts/dev-api.ps1`](scripts/dev-api.ps1) - Start backend with env vars
- [`scripts/init_local_db.py`](scripts/init_local_db.py) - Initialize DB schema
- [`scripts/seed_evalforge_universe.py`](scripts/seed_evalforge_universe.py) - Seed data

### Database
- [`arcade_app/database.py`](arcade_app/database.py) - DB engine & init_db()
- [`arcade_app/models.py`](arcade_app/models.py) - SQLModel definitions

### App Entry Points
- [`arcade_app/agent.py`](arcade_app/agent.py) - FastAPI app with lifespan
- [`apps/web/src/main.tsx`](apps/web/src/main.tsx) - React app entry

---

## 🎯 Next Steps

Once local dev is running:

1. **Edit Quest Content:**
   - Quests are in `data/quests.json`
   - Re-run `pnpm dev:seed` to update DB

2. **Add New Bosses:**
   - Define in `data/bosses/`
   - Update seed script
   - Re-seed

3. **Modify Frontend:**
   - Edit components in `apps/web/src/`
   - HMR (Hot Module Reload) is enabled

4. **Test Backend Changes:**
   - Backend auto-reloads with `--reload` flag
   - Check logs in terminal

5. **Run Tests:**
   ```powershell
   pnpm test:api   # Backend (pytest)
   pnpm test:web   # Frontend (vitest)
   ```

---

## 🚢 Production vs Development

| Feature | Development | Production |
|---------|-------------|------------|
| Database | localhost:5435 | Cloud SQL |
| Redis | localhost:6379 | Cloud Memorystore |
| Auth | Fake user (dev-user) | GitHub OAuth |
| Auto-init DB | Optional (AUTO_INIT_DB=1) | Disabled |
| Hot Reload | Enabled | Disabled |
| Frontend Proxy | Vite → localhost:8092 | Built static files |

---

## 🎉 You're All Set!

Local dev is **painless and fast**. Any questions? Check the [walkthrough](../../.gemini/antigravity/brain/6537e8fc-dd2f-4716-8923-94272960d97e/walkthrough.md) or ask in the team chat.

**Happy coding!** 🚀
