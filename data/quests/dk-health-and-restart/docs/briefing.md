# Briefing: Health Checks and Restart Policies

The stack runs, but it's brittle. If the database takes a moment to start, the API crashes and never recovers. If either container exits due to a transient error, it stays down forever.

## Mission

1. **Add a HEALTHCHECK** to the `db` service so Docker can report when Postgres is ready to accept connections:
   ```yaml
   healthcheck:
     test: ["CMD-SHELL", "pg_isready -U postgres"]
     interval: 10s
     timeout: 5s
     retries: 5
   ```

2. **Set restart policies** on both services so they recover automatically:
   ```yaml
   restart: unless-stopped
   ```

3. **Upgrade depends_on** so the API only starts once the DB is confirmed healthy:
   ```yaml
   depends_on:
     db:
       condition: service_healthy
   ```
