# Infra World — Extra Directories Audit

Date: 2026-02-12  
World: world-infra  
Canonical Questpack: `data/questpacks/infra_core.json` (LOCKED @ 10 quests)

## Goal

Infra core is production-bound and must remain stable. This audit classifies non-pack directories into:
- **Deprecate (Alias):** duplicates/older naming → redirect to canonical core quest
- **Promote (Future Pack):** valid expansion content → Tier 2 pack (infra_plus)
- **Hold (Future / Policy):** too broad or needs deterministic test feasibility review

---

## Canonical Core Pack (10 quests)

These are the only slugs in `infra_core.json`:

- infra-ignition
- infra-ports-and-localhost
- infra-env-config
- infra-healthchecks
- infra-logs-metrics
- infra-docker-compose
- infra-networking-dns
- infra-reverse-proxy
- infra-cors-cookies
- infra-debug-playbook

Pack Stability Rule: **Do not add/remove/rename these slugs** during Phase A.

---

## Discovered Extra Directories

### In `data/quests/` (extra beyond core pack)
- infra-ci-smoke
- infra-compose-basics
- infra-dockerfile-basics
- infra-env-secrets
- infra-images-containers
- infra-networks
- infra-ports-localhost
- infra-volumes

### In `docs/quests/` (extra beyond core pack)
- infra-ci-cd-basics
- infra-container-networking
- infra-containment-q1-linux-shell-and-fs
- infra-deployment-strategies
- infra-docker-basics
- infra-env-variables
- infra-kubernetes-intro
- infra-monitoring-logging
- infra-service-q1-dockerize-and-compose
- infra-volumes-persistence

Notes:
- All 10 core slugs exist in both `data/quests/` and `docs/quests/`.
- Extras are split: some exist only in data, others only in docs.

---

## Decisions Table

| Directory | Location | Decision | Redirect / Target | Reason | Phase A Action |
|---|---|---:|---|---|---|
| infra-ports-localhost | data | Deprecate (Alias) | infra-ports-and-localhost | Naming drift; same concept | Add DEPRECATED.md + stop referencing |
| infra-compose-basics | data | Deprecate (Alias) | infra-docker-compose | Compose basics covered by canonical | Add DEPRECATED.md + stop referencing |
| infra-networks | data | Deprecate (Alias) | infra-networking-dns | Network/DNS mapping overlaps canonical | Add DEPRECATED.md + stop referencing |
| infra-env-variables | docs | Deprecate (Alias) | infra-env-config | Same topic, cleaner canonical slug | Add DEPRECATED.md |
| infra-monitoring-logging | docs | Deprecate (Alias) | infra-logs-metrics | Overlaps canonical observability quest | Add DEPRECATED.md |
| infra-container-networking | docs | Hold (Future/Review) | (TBD) | Broader than DNS-only; may span ports/proxy | Keep as candidate for Tier 2 |
| infra-ci-smoke | data | Promote (Future Pack) | infra_plus.json | Useful but not core; needs deterministic harness | Move to Tier 2 pack later |
| infra-ci-cd-basics | docs | Promote (Future Pack) | infra_plus.json | Good expansion; requires clear scope | Add refinement packet later |
| infra-docker-basics | docs | Promote (Future Pack) | infra_plus.json | Strong Tier 2 onboarding | Add refinement packet later |
| infra-dockerfile-basics | data | Promote (Future Pack) | infra_plus.json | Valuable; needs test harness design | Add refinement packet later |
| infra-images-containers | data | Promote (Future Pack) | infra_plus.json | Good expansion content | Add refinement packet later |
| infra-env-secrets | data | Promote (Future Pack) | infra_plus.json | Good but policy-sensitive (avoid real secrets) | Add refinement packet later |
| infra-volumes | data | Promote (Future Pack) | infra_plus.json | Useful expansion | Add refinement packet later |
| infra-volumes-persistence | docs | Promote (Future Pack) | infra_plus.json | Pairs with infra-volumes | Merge/align later |
| infra-service-q1-dockerize-and-compose | docs | Hold (Future/Review) | (TBD) | "Q1" style content may not match Tier 1 patterns | Keep until pack strategy decided |
| infra-deployment-strategies | docs | Hold (Future/Review) | (TBD) | Too high-level; needs deterministic tasks | Keep |
| infra-kubernetes-intro | docs | Hold (Future/Review) | (TBD) | External deps + environment complexity | Keep |
| infra-containment-q1-linux-shell-and-fs | docs | Hold (Future/Review) | (TBD) | Out-of-scope for infra_core | Keep |

---

## Phase A Checklist (Now)

### 1) Deprecation Notices
Create DEPRECATED.md in each alias directory (docs and/or data):
- data/quests/infra-ports-localhost/DEPRECATED.md
- data/quests/infra-compose-basics/DEPRECATED.md
- data/quests/infra-networks/DEPRECATED.md
- docs/quests/infra-env-variables/DEPRECATED.md
- docs/quests/infra-monitoring-logging/DEPRECATED.md

### 2) Pack Stability
- Do NOT add extra directories to `infra_core.json`
- Do NOT rename canonical slugs

### 3) Verify
- Ensure nothing references deprecated directories (docs links, tooling, etc.)
- Keep infra_core 10-quest pack as the only "production" infra pack

---

## Phase B Plan (Later)

### Promote → `infra_plus.json` (Tier 2)
Candidate set:
- infra-ci-smoke
- infra-ci-cd-basics
- infra-docker-basics
- infra-dockerfile-basics
- infra-images-containers
- infra-env-secrets
- infra-volumes
- infra-volumes-persistence

Implementation steps:
1) Write refinement packets (README + tests + fixtures + solutions)
2) Enforce deterministic harness (no network, no docker daemon dependence)
3) Add new questpack `data/questpacks/infra_plus.json`

### Hold (Review)
- infra-kubernetes-intro
- infra-deployment-strategies
- infra-service-q1-dockerize-and-compose
- infra-containment-q1-linux-shell-and-fs
- infra-container-networking

Gate: must be testable without external services and fit EvalForge quest UX patterns.

---

## Acceptance Criteria

- No changes to `infra_core.json` quest list
- Deprecated directories have clear redirects
- Future content is documented but not activated in core pack
