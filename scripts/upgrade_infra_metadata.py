from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "data" / "questpacks" / "infra_core.json"

VERSION = "2026-02-12.v1"
SOURCE = "infra_metadata_upgrade"

def q(slug: str, mission: str, objective: str, objectives: list[str], concept: str, guided: str, solution: str, lore: str):
  return {
    "slug": slug,
    "briefing_md": f"# Mission: {mission}\n\n**Objective:** {objective}\n\nYou will implement the required behavior in `workspace/task.sh`.\nYour script must read from `fixtures/` (or the quest's fixture files) and write deterministic outputs to `outputs/`.\n\n",
    "objectives": [
      {"id": f"obj_{slug.replace('-','_')}_{i+1}", "text": t, "why": "Test-aligned requirement"} for i, t in enumerate(objectives)
    ],
    "lore_md": f"## Ops Deck Log\n\n> *Booting infra simulation…*\n>\n{lore}\n\n**Constraint:** No network calls. Pure file parsing + deterministic output.\n",
    "tiered_hints": {
      "concept": concept,
      "guided": guided,
      "full_solution": solution
    },
    "content_source": SOURCE,
    "content_version": VERSION
  }

UPDATES = {
  "infra-ignition": q(
    "infra-ignition",
    "Preflight Checks",
    "Generate a preflight report and exit with the correct code when tools are missing.",
    [
      "Read required tools and installed tools from fixtures",
      "Write outputs/preflight.txt with STATUS and MISSING fields",
      "Exit 10 and print MISSING_TOOLS on stderr when missing tools exist",
      "Exit 0 when everything is present"
    ],
    "Think of this like a CI preflight: diff required vs installed and report missing.",
    "Normalize newlines, build a missing list, join with commas, and follow the exact output format.",
    "Approach: read both lists, compute missing = required - installed, write outputs/preflight.txt, then exit 10 with stderr message if missing else 0.",
    "> Systems won't deploy if your baseline tools aren't installed. The pipeline expects a strict preflight contract."
  ),
  "infra-ports-and-localhost": q(
    "infra-ports-and-localhost",
    "Port Mapping Sanity",
    "Analyze port mappings and explain what is reachable from localhost vs container network.",
    [
      "Parse the provided fixture(s) describing port mappings",
      "Write the expected analysis file to outputs",
      "Correctly identify host vs container ports",
      "Preserve ordering exactly as fixtures define"
    ],
    "Port mapping is about translating HOST:PORT -> CONTAINER:PORT and knowing which side traffic starts on.",
    "Treat each mapping line as data. Extract both sides. Output in the exact requested format and order.",
    "Approach: parse mappings, write outputs with normalized lines; do not invent ports or reorder rows.",
    "> The lab router lights up. If you misread ports, you ship a service nobody can reach."
  ),
  "infra-env-config": q(
    "infra-env-config",
    "Env Config Loader",
    "Load environment-style config and emit a normalized resolved configuration.",
    [
      "Read key/value pairs from fixtures",
      "Apply defaults/overrides as described in the quest README",
      "Write normalized config output to outputs",
      "Handle missing keys deterministically"
    ],
    "Env config is parsing + precedence: defaults < file < overrides.",
    "Split on the first '=' only; trim spaces; ignore blank lines/comments if present.",
    "Approach: build a dict of resolved values, emit sorted or spec-ordered output (match README/tests).",
    "> The service won't start without correct env. Your job is to make config resolution predictable."
  ),
  "infra-healthchecks": q(
    "infra-healthchecks",
    "Healthcheck Aggregator",
    "Summarize service health from a raw fixture list into a report + score.",
    [
      "Read fixtures/health.txt (or equivalent) and parse name/status/latency",
      "Write outputs/health_status.txt with STATUS/FAILED/SLOWEST fields",
      "Write outputs/health_score.txt as an integer percent",
      "Preserve deterministic formatting and ordering"
    ],
    "This is a reducer: map inputs → counts → derived status + slowest.",
    "Track failed services, compute ok/total, find max latency, then format output exactly.",
    "Approach: parse rows, compute failures list, compute slowest, compute score, write both outputs.",
    "> Dashboards are down. The incident commander needs one clean summary file."
  ),
  "infra-logs-metrics": q(
    "infra-logs-metrics",
    "Log Signal Extractor",
    "Extract key metrics from logs and emit a compact report.",
    [
      "Parse the fixture log file(s) deterministically",
      "Count/aggregate the required signals (errors, warnings, p95, etc as README specifies)",
      "Write outputs report files with exact formatting",
      "Avoid non-determinism (no timestamps, no random ordering)"
    ],
    "Logs become metrics when you count and bucket them consistently.",
    "Use grep/awk/sed defensively; normalize CRLF; keep stable ordering.",
    "Approach: parse, aggregate, write outputs; match the test's exact expected text.",
    "> Observability is a contract. Your parser turns chaos into a stable metric stream."
  ),
  "infra-docker-compose": q(
    "infra-docker-compose",
    "Compose Inspector",
    "Extract a structured view of a docker-compose file (services/ports/env/etc) into outputs.",
    [
      "Read the compose fixture(s) and extract requested fields",
      "Write the output summary file(s) to outputs",
      "Keep services in spec order (or deterministic order per README)",
      "Handle missing optional fields safely"
    ],
    "Compose parsing is mostly pattern extraction from YAML-like structure (in this simplified lab).",
    "Don't fully YAML-parse unless required; use stable string parsing suited to the fixture constraints.",
    "Approach: identify service blocks, extract known keys, emit normalized summary.",
    "> A deployment is failing. You need a quick machine-readable summary of what compose is doing."
  ),
  "infra-networking-dns": q(
    "infra-networking-dns",
    "DNS + Network Map",
    "Build a connectivity map from fixtures describing networks, aliases, and service names.",
    [
      "Parse the provided network fixture(s)",
      "Determine which services can resolve which names",
      "Write the expected outputs mapping file",
      "Preserve deterministic order"
    ],
    "DNS in docker networks is name → container IP (conceptually). The lab simplifies to name/alias mapping.",
    "Treat each alias mapping as an edge in a graph; emit the expected resolved names list.",
    "Approach: parse mappings, expand aliases, output in a stable order.",
    "> The tunnel is up, but requests 404. It's usually DNS. Your map tells the truth."
  ),
  "infra-reverse-proxy": q(
    "infra-reverse-proxy",
    "Nginx Route Extractor",
    "Parse nginx location → proxy_pass routes and write them in order.",
    [
      "Read the nginx config fixture",
      "Extract each `location <path>` and its `proxy_pass <target>`",
      "Write outputs/routes.txt as `<path> -> <target>` per line",
      "Preserve file order exactly"
    ],
    "Reverse proxies are routing tables. Extract routes without reformatting the source.",
    "Scan for `location` then the next `proxy_pass` inside that block; emit a mapping line when both are found.",
    "Approach: minimal state machine (location_path + proxy_target) using awk is perfect here.",
    "> Requests enter the proxy first. If routes are wrong, the whole stack is unreachable."
  ),
  "infra-cors-cookies": q(
    "infra-cors-cookies",
    "CORS + Cookie Policy",
    "Evaluate a policy fixture and output which origins/cookies are allowed.",
    [
      "Parse the CORS/cookie fixture input",
      "Determine allow/deny results per the README rules",
      "Write outputs with exact expected values",
      "Handle edge cases like wildcard vs explicit allowlists deterministically"
    ],
    "CORS is a browser-side gate; cookies are transport constraints (Domain/SameSite/Secure).",
    "Implement explicit precedence rules from the README; don't guess or infer beyond fixtures.",
    "Approach: parse rules, apply to each test case row, emit outputs exactly.",
    "> Security review flags your API. Your job: make the policy machine-checkable."
  ),
  "infra-debug-playbook": q(
    "infra-debug-playbook",
    "Debug Triage Generator",
    "Given an incident fixture, generate a short runbook-like triage output.",
    [
      "Parse the incident symptoms from fixtures",
      "Classify the likely failure class (ports, DNS, CORS, proxy, env, etc.)",
      "Write the requested runbook/triage outputs",
      "Keep output stable and rubric-aligned"
    ],
    "A good runbook is a decision tree: symptoms → checks → likely fix.",
    "Use simple matching rules based on fixture signals; emit exactly what tests expect.",
    "Approach: map symptoms to a primary diagnosis and recommended checks; write outputs.",
    "> Pager goes off. You have 90 seconds to propose the next best debugging step."
  ),
}

def main() -> int:
  data = json.loads(PACK.read_text(encoding="utf-8"))
  if not isinstance(data, dict) or "quests" not in data:
    raise SystemExit("infra_core.json unexpected format (expected {world_id, track_id, title, quests})")

  quests = data["quests"]
  out = []
  for qobj in quests:
    slug = qobj.get("slug")
    if slug in UPDATES:
      upd = UPDATES[slug]
      # preserve any extra fields not in our patch
      qobj.update(upd)
    out.append(qobj)

  data["quests"] = out
  PACK.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
  print(f"[OK] upgraded infra metadata for {len(UPDATES)} quests → {PACK}")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
