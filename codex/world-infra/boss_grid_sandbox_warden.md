# Boss Codex – Grid Sandbox Warden

- **Boss ID:** `boss-grid-containment-sandbox-warden`
- **World:** `world-infra` – The Grid
- **Track:** `grid-containment`
- **Stage:** `stage-1-grid-containment`
- **Title:** Sandbox Warden
- **Tier:** Containment Boss (Stage 1 Capstone)

---

## Lore

At the edge of The Grid lies an isolated host, an experimental **Sandbox** where stacks are born before they are allowed into the main lattice.

The **Sandbox Warden** watches this host relentlessly.

It has no patience for:
- “It works on my machine” without real logs,
- servers that bind to nothing and listen on nowhere,
- disks quietly filling up until the node begins to thrash.

To pass, you must prove you can bring a sick host back to health using only:
- the CLI,
- the logs,
- and your own mental model of how services live and die.

---

## Attacks

The Sandbox Warden attacks by breaking assumptions about a *single* Linux host.

### 1. Port of No Return

- **Symptom:** Service is “running” according to systemd, but nobody can reach it.
- **In game:** Liveness checks fail; curl times out; uptime seems fine.
- **What it tests:** Understanding of ports, listeners, bind addresses, and firewall rules.

---

### 2. Log Choke

- **Symptom:** Disk usage spikes; processes start failing writes.
- **In game:** The host logs complain about “No space left on device”, log rotation is misconfigured, and the service crashes frequently.
- **What it tests:** Ability to inspect file systems, identify large or runaway logs, and clean up without nuking important data.

---

### 3. Zombie Swarm

- **Symptom:** CPU and memory spike randomly; multiple stale processes linger.
- **In game:** Old deploys left processes behind; systemd service definitions are half-misconfigured; restarts don’t actually clean things up.
- **What it tests:** Process inspection, service management, and understanding how supervised processes should behave.

---

### 4. Silent Misconfig

- **Symptom:** The “correct” service is running… but it’s reading the wrong config or environment.
- **In game:** The app still points to a staging DB, wrong port, or outdated feature flags.
- **What it tests:** Ability to correlate config files, env vars, process args, and logs into a coherent picture.

---

## Strategy

To defeat the Sandbox Warden, the player must demonstrate:

1. **System Orientation**
   - Quickly identify OS, key services, and relevant logs.
   - Use core tools: `ls`, `df`, `du`, `ps`, `top/htop`, `journalctl`, `netstat/ss`, `lsof`.

2. **Network and Port Insight**
   - Check whether a process is actually listening on the expected port and interface.
   - Validate connectivity with `curl`, `nc`, or similar.
   - Recognize firewall or bind-address misconfigurations.

3. **Service & Process Hygiene**
   - Manage services using `systemd` or the local init system.
   - Kill or drain stale processes safely.
   - Ensure service definitions (ExecStart, WorkingDirectory, env) match the intended deployment.

4. **On-Call-Ready Runbooks**
   - Present a clear, step-by-step triage path.
   - Use commands that can be safely copied and pasted.
   - Leave the host in a clean, documented state.

---

## Boss Fight Shape

- **Submission Format:** A Markdown runbook with clearly labeled sections:
  - `## Incident Summary`
  - `## Phase 1 – Triage`
  - `## Phase 2 – Deep Dive`
  - `## Phase 3 – Fix & Verification`
- **Perspective:** You are the on-call engineer responding to an incident page for the Sandbox host.
- **Scenario (encoded for the player):**
  - A single VM running:
    - `api.service` (your app),
    - `nginx.service` as reverse proxy.
  - Symptoms:
    - Health checks to `https://sandbox.example.internal/health` are failing.
    - Alerts about high disk usage on `/var`.
    - Occasional spikes in CPU.

The correct submission will:

- Show command sequences to **triage** (what do you run, in which order, and why).
- Show how you **narrow down** root causes for port issues, disk pressure, and zombie processes.
- Show how you **fix** them and confirm the Sandbox is healthy.
