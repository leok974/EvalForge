# Operation Skyhook: Deployment Runbook

**Target**: Google Compute Engine (GCE) VM
**OS**: Debian 11 / Ubuntu 22.04 LTS
**Status**: READY FOR DEPLOY

## 1. VM Requirements
- **Machine Type**: e2-standard-2 (2 vCPU, 8GB RAM) minimum.
- **Disk**: 50GB+ SSD (pd-balanced).
- **Firewall**: Allow HTTP (80), HTTPS (443), and custom port 8080 if testing directly.
- **Service Account**: Must have permissions to pull from Artifact Registry (if using private images) or access Vertex AI.

## 2. Initial Setup
SSH into the VM and install Docker + Compose.

```bash
# Update and install dependencies
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify
sudo docker run hello-world
```

## 3. Deployment
Clone the repo or copy the necessary files (`docker-compose.prod.yml`, `.env.prod`, `Dockerfile`, `arcade_app/`, `apps/web/`, `data/`).

```bash
# 1. Create .env.prod
cat <<EOF > .env.prod
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
EVALFORGE_MODEL_VERSION=gemini-2.5-flash-001
EVALFORGE_MOCK_GRADING=0
DB_PASSWORD=secure_password_here
SECRET_KEY=generate_a_secure_random_key
EOF

# 2. Build and Launch
sudo docker compose -f docker-compose.prod.yml up -d --build
```

## 4. Initialization (First Run Only)
Initialize the database and seed content.

```bash
# 1. Run Migrations (if using Alembic, otherwise init_db handles it on startup)
# sudo docker compose -f docker-compose.prod.yml exec app alembic upgrade head

# 2. Seed Curriculum
sudo docker compose -f docker-compose.prod.yml exec app python scripts/seed_curriculum.py

# 3. Seed Bosses
sudo docker compose -f docker-compose.prod.yml exec app python -c "import asyncio; from arcade_app.seed_bosses import seed_bosses; asyncio.run(seed_bosses())"

# 4. Ingest Codex
sudo docker compose -f docker-compose.prod.yml exec app python scripts/ingest_codex.py
```

## 5. Verification
Check system health.

```bash
# 1. Check Containers
sudo docker compose -f docker-compose.prod.yml ps

# 2. Check Logs
sudo docker compose -f docker-compose.prod.yml logs -f app

# 3. Verify Readiness Endpoint
curl http://localhost:8080/api/ready
# Expected: {"status": "ready", "components": {"database": "ok", "redis": "ok"}}
```

## 6. GCP Edge Setup (CLI Only)

This section describes how to bring EvalForge online on GCE **only via CLI** (no web console).

### 0. Prereqs

- `gcloud` CLI installed and authenticated:
  ```bash
  gcloud auth login
  gcloud auth application-default login   # optional but useful
  ```
- You have a domain you control (e.g. `leoklemet.com`) where you can edit DNS.

Set your project/region/zone once:

```bash
export PROJECT_ID="evalforge-480016"
export REGION="us-central1"
export ZONE="us-central1-a"
export VM_NAME="evalforge-vm"
export STATIC_IP_NAME="evalforge-ip"
export DOMAIN="evalforge.com"  # Change this to your actual domain

gcloud config set project "$PROJECT_ID"
gcloud config set compute/region "$REGION"
gcloud config set compute/zone "$ZONE"
```

### 1. Create the EvalForge VM (if not created yet)

```bash
gcloud compute instances create "$VM_NAME" \
  --machine-type=e2-standard-2 \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --tags=http-server,https-server \
  --boot-disk-size=100GB
```

> The `http-server,https-server` tags will be used by Google’s default firewall rules.
> If you prefer explicit rules, see step 3.

SSH in:

```bash
gcloud compute ssh "$VM_NAME"
```

### 2. Reserve a static external IP and attach it

Reserve the IP (once):

```bash
gcloud compute addresses create "$STATIC_IP_NAME" \
  --region="$REGION"
```

Get the IP value:

```bash
gcloud compute addresses describe "$STATIC_IP_NAME" \
  --region="$REGION" \
  --format="value(address)"
```

Attach it to the VM’s NIC:

```bash
# Remove existing ephemeral IP config
gcloud compute instances delete-access-config "$VM_NAME" \
  --access-config-name="external-nat" \
  --zone="$ZONE"

# Add access config with reserved IP
gcloud compute instances add-access-config "$VM_NAME" \
  --network-interface="nic0" \
  --address="$STATIC_IP_NAME" \
  --zone="$ZONE"
```

### 3. Firewall rules (CLI)

If you didn’t rely on the default `allow-http` / `allow-https` rules, create explicit ones:

```bash
gcloud compute firewall-rules create evalforge-allow-http \
  --allow=tcp:80 \
  --target-tags=http-server \
  --description="Allow HTTP for EvalForge" \
  --direction=INGRESS

gcloud compute firewall-rules create evalforge-allow-https \
  --allow=tcp:443 \
  --target-tags=https-server \
  --description="Allow HTTPS for EvalForge" \
  --direction=INGRESS
```

Make sure the instance has those tags (`http-server,https-server` as in step 1).

### 4. DNS (manual but CLI-assist)

From step 2, you have the static IP, e.g.:

```bash
gcloud compute addresses describe "$STATIC_IP_NAME" \
  --region="$REGION" \
  --format="value(address)"
```

In your DNS provider (e.g. Cloudflare, Namecheap), create these records:

1. **Root Domain (@)**
   * Type: `A`
   * Value: `<STATIC_IP>`
   * TTL: 300–3600

2. **WWW Subdomain (www)**
   * Type: `A` (or CNAME to @)
   * Value: `<STATIC_IP>` (or `@`)

You can verify propagation from your local machine:

```bash
nslookup "$DOMAIN"
```

### 5. Install Docker + docker compose on the VM

SSH into the VM:

```bash
gcloud compute ssh "$VM_NAME"
```

Install Docker (example using the convenience script):

```bash
sudo apt-get update
curl -fsSL https://get.docker.com | sudo sh

# Optional: allow current user to run docker
sudo usermod -aG docker "$USER"
newgrp docker
```

Verify:

```bash
docker ps
```

### 6. Pull EvalForge code and configure env

On the VM:

```bash
sudo mkdir -p /opt/evalforge
sudo chown "$USER" /opt/evalforge
cd /opt/evalforge

git clone https://github.com/<you>/evalforge.git .
```

Create `.env.prod`:

```bash
cat > .env.prod << 'EOF'
ENV=prod
EVALFORGE_DB_PASSWORD=change-me
DATABASE_URL=postgresql+psycopg2://evalforge:${EVALFORGE_DB_PASSWORD}@db:5432/evalforge
REDIS_URL=redis://redis:6379/0
SECRET_KEY=change-me-too
# LLM keys if needed
EOF
```

### 7. Start core services and run migrations

Bring up DB + Redis first:

```bash
docker compose -f docker-compose.prod.yml up -d db redis
```

Run DB migrations:

```bash
docker compose -f docker-compose.prod.yml run --rm app \
  alembic upgrade head
```

Ingest Codex + curriculum:

```bash
docker compose -f docker-compose.prod.yml run --rm app \
  python -m scripts.ingest_codex

docker compose -f docker-compose.prod.yml run --rm app \
  python -m scripts.seed_curriculum
```

(Optional) Seed a demo user:

```bash
docker compose -f docker-compose.prod.yml run --rm app \
  python -m scripts.seed_demo_user
```

### 8. Bring up app, worker, and nginx

```bash
docker compose -f docker-compose.prod.yml up -d app worker nginx
```

Check containers:

```bash
docker ps
```

Smoke test (HTTP, before TLS):

```bash
curl -s "http://$DOMAIN/api/ready"
```

You should see the JSON payload or a redirect to HTTPS after cert issuance.

### 9. Issue TLS certificates via certbot (CLI, in Docker)

Still on the VM, run:

```bash
cd /opt/evalforge

docker compose -f docker-compose.prod.yml run --rm certbot \
  certonly --webroot \
  -w /var/www/certbot \
  -d "$DOMAIN" -d "www.$DOMAIN" \
  --email you@example.com \
  --agree-tos \
  --non-interactive
```

Restart nginx to load the new certs:

```bash
docker compose -f docker-compose.prod.yml restart nginx
```

Verify HTTPS:

```bash
curl -s "https://$DOMAIN/api/ready" | jq .
```

You should see `{ "status": "ok", ... }`.

### 10. E2E readiness test (Python CLI)

From `/opt/evalforge`:

```bash
python -m pytest tests/e2e/test_ready.py
```

If this passes, the stack (app + DB + Redis + edge) is healthy.

### 11. Auto-renew TLS via cron (CLI)

Edit the crontab:

```bash
crontab -e
```

Add:

```cron
0 3 * * * cd /opt/evalforge && docker compose -f docker-compose.prod.yml run --rm certbot renew && docker compose -f docker-compose.prod.yml restart nginx
```

This will renew certificates nightly and reload nginx if anything changed.

## 7. Troubleshooting
- **Database Connection**: Check `docker compose logs db`. Ensure `pgvector` image pulled correctly.
- **Vertex AI Auth**: Ensure VM service account has `Vertex AI User` role.
- **Frontend Assets**: If 404s on assets, check `docker compose exec app ls -l /app/static`.
- **SSL Failures**: Check `docker compose logs certbot`. Ensure DNS resolves to the VM's IP and port 80 is open.
