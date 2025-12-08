# Boss: Sandbox Warden – Golden Runbook

> Reference solution for the `boss-grid-containment-sandbox-warden` encounter.
> Scenario: Single Linux VM running `api.service` behind `nginx.service`.

---

## Incident Summary

- **Service:** `sandbox-api` (systemd unit: `api.service`)
- **Ingress:** `nginx.service` → `https://sandbox.example.internal`
- **Symptoms:**
  - Health checks to `https://sandbox.example.internal/health` are failing.
  - Users report timeouts when calling the API.
  - Alerts show **disk usage > 90% on `/var`** and occasional **CPU spikes**.

**Goal:** Restore the Sandbox host to a healthy state and document a repeatable triage / remediation path.

---

## Phase 1 – Fast Triage

1. **Verify the host is reachable**

```bash
ping -c 3 sandbox.example.internal
ssh core@sandbox.example.internal
```

2. **Check basic host health**

```bash
# CPU / memory snapshot
top -o %CPU

# Disk usage by filesystem
df -h

# Quick view of system load and uptime
uptime
```

3. **Verify the symptom from the host**

```bash
# Hit the health endpoint from inside the box
curl -vk https://sandbox.example.internal/health
```

* Note whether this fails with:

  * connection refused → nothing listening or nginx down,
  * TLS/hostname issues,
  * 5xx error → app responding but unhealthy.

---

## Phase 2 – Deep Dive

### A. Ports & Listeners

4. **Check which services are listening**

```bash
# Show listening sockets with process info
sudo ss -tulpen | head -n 50
```

* Confirm:

  * `nginx` is listening on `*:443` (or the configured port),
  * `api.service` is listening on its expected port (e.g. `127.0.0.1:8000`).

5. **Confirm API is reachable from nginx**

```bash
# Hit API directly (bypassing nginx) if it binds locally
curl -v http://127.0.0.1:8000/health
```

* If this fails, the problem is likely in `api.service` itself.
* If this succeeds, focus on nginx config or TLS.

---

### B. Services & Processes

6. **Inspect systemd status**

```bash
sudo systemctl status api.service
sudo systemctl status nginx.service
```

* Look for:

  * recent restarts,
  * non-zero exit codes,
  * environment or WorkingDirectory issues.

7. **Inspect processes directly**

```bash
ps aux | egrep 'api|nginx' | grep -v grep
```

* Ensure there is a single expected process tree (no zombie copies).
* If multiple old versions are running, note PIDs for cleanup later.

---

### C. Logs & Errors

8. **Systemd journal for API**

```bash
sudo journalctl -u api.service --since "10 minutes ago"
```

9. **Systemd journal for nginx**

```bash
sudo journalctl -u nginx.service --since "10 minutes ago"
```

10. **App logs (if separate)**

```bash
# Example: adjust path to actual app log directory
sudo ls -lh /var/log/sandbox-api/
sudo tail -n 100 /var/log/sandbox-api/app.log
```

* Look for:

  * Exceptions,
  * port binding errors,
  * DB / upstream failures,
  * “No space left on device”.

---

### D. Disk Pressure (Log Choke)

11. **Confirm disk saturation**

```bash
df -h / /var
```

12. **Find largest directories under /var**

```bash
sudo du -xh /var | sort -h | tail -n 20
```

* Pay special attention to:

  * `/var/log/`
  * `/var/lib/docker/` (if Docker is present)
  * `/var/tmp/`

13. **Inspect log growth**

```bash
sudo du -xh /var/log | sort -h | tail -n 20
```

* Identify log files that are unexpectedly huge, e.g.:

  * `/var/log/nginx/access.log`
  * `/var/log/nginx/error.log`
  * `/var/log/sandbox-api/app.log`

---

## Phase 3 – Fix & Verification

### A. Disk Cleanup (Safe)

14. **Rotate or compress large logs**

Instead of deleting blindly, rotate and compress:

```bash
# Example: truncate a known safe log
sudo truncate -s 0 /var/log/nginx/access.log

# Or move/zip an old app log
sudo mv /var/log/sandbox-api/app.log /var/log/sandbox-api/app.log.$(date +%F)
sudo gzip /var/log/sandbox-api/app.log.$(date +%F)
```

15. **Re-check disk usage**

```bash
df -h /var
```

> Goal: bring `/var` usage below ~80%.

16. **(Optional) Improve logrotate config**

```bash
sudo cat /etc/logrotate.d/nginx
sudo cat /etc/logrotate.d/sandbox-api || true
```

* Ensure logrotate is configured with reasonable rotation and retention.
* Add/update a config if missing (document in a follow-up PR).

---

### B. Fix Service / Port Issues

17. **Verify API bind address and port**

Check service unit and config:

```bash
sudo systemctl cat api.service
grep -R "BIND_ADDRESS" -n /etc/sandbox-api/ /opt/sandbox-api/ 2>/dev/null || true
```

* Confirm that:

  * The app binds to `127.0.0.1:8000` (or your chosen address).
  * Env vars / config files match what nginx expects.

18. **Check nginx upstream configuration**

```bash
sudo grep -R "sandbox-api" -n /etc/nginx
sudo grep -R "proxy_pass" -n /etc/nginx/sites-enabled/ /etc/nginx/conf.d/
```

* Confirm upstream block points to the API’s actual host/port.

Example snippet:

```nginx
upstream sandbox_api {
    server 127.0.0.1:8000;
}

server {
    listen 443 ssl;
    server_name sandbox.example.internal;

    location / {
        proxy_pass http://sandbox_api;
        ...
    }
}
```

19. **Reload configuration & restart services**

```bash
sudo nginx -t
sudo systemctl reload nginx

sudo systemctl restart api.service
sudo systemctl restart nginx.service
```

* `nginx -t` verifies config before reload.

---

### C. Verify Recovery

20. **Health checks from host**

```bash
curl -vk https://sandbox.example.internal/health
```

21. **Health checks from outside (if possible)**

Run from monitoring box or your laptop (through VPN/tunnel):

```bash
curl -vk https://sandbox.example.internal/health
```

22. **Re-check host vitals**

```bash
df -h /var
top -o %CPU
sudo journalctl -u api.service -u nginx.service --since "5 minutes ago"
```

* Confirm:

  * Disk < 80%,
  * CPU stable,
  * No new errors in logs.

---

## Final Notes & Follow-Ups

* **Postmortem notes:**

  * Root cause: `app.log` and `nginx access.log` grew without rotation, causing disk saturation and app write failures.
  * Secondary impact: API could not write logs, leading to crashes and health check failures.
* **Follow-up tasks:**

  * Tighten logrotate and retention policy.
  * Add disk usage alerts earlier (e.g., warning at 75%).
  * Add a synthetic check that directly hits `127.0.0.1:8000/health` to distinguish nginx vs app failures.

This runbook is meant to be **copy-paste safe** and serves as the golden reference for the Sandbox Warden boss.
