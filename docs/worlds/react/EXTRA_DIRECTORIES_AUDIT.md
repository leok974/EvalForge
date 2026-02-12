# React Extra Directories Audit

**Date**: 2026-02-12  
**Questpack**: `data/questpacks/react_core.json` (10 quests)  
**Extra Directories Found**: 8 in `docs/quests/react-*`

## Policy

✅ **Phase A (Now)**: Keep `react_core.json` stable at 10 quests. Do NOT add extras during core refinement.  
🔮 **Phase B (Later)**: After core verification passes, promote selected extras to `react_plus.json` or deprecate.

---

## Audit Decisions

| Directory | Action | Canonical Quest | Reason |
|-----------|--------|-----------------|--------|
| `react-effects` | **Deprecate (alias)** | `react-effects-mount` | Overlaps with mount lifecycle quest |
| `react-context` | **Deprecate (alias)** | `react-context-theme` | Generic name; pack uses theme-focused version |
| `react-state` | **Deprecate (alias)** | `react-state-counter` / `react-state-toggle` | Generic umbrella; pack has split fundamentals |
| `react-lists-keys` | **Deprecate (alias)** | `react-lists` | Keys explicitly covered in react-lists |
| `react-events` | **Promote → react_plus.json** | `react-events` (new) | Core skill; good for expansion pack |
| `react-custom-hooks` | **Promote → react_plus.json** | `react-custom-hooks` (new) | Intermediate tier-2 skill |
| `react-routing` | **Hold / Future** | TBD | Requires react-router dependency |
| `react-performance-basics` | **Hold / Future** | TBD | Advanced; needs deterministic perf tests |

---

## Action Items

### Aliases to Deprecate (4 directories)

- [ ] **react-effects**
  - Diff vs `react-effects-mount`
  - Merge better explanations into canonical docs
  - Add `DEPRECATED.md` → redirect to `react-effects-mount`

- [ ] **react-context**
  - Diff vs `react-context-theme`
  - Extract improvements into canonical quest
  - Add `DEPRECATED.md` → redirect to `react-context-theme`

- [ ] **react-state**
  - Diff vs `react-state-counter` + `react-state-toggle`
  - Split tutorial content across both canonical quests
  - Add `DEPRECATED.md` → redirect to both

- [ ] **react-lists-keys**
  - Diff vs `react-lists`
  - Merge key explanations into `react-lists` tutorial
  - Add `DEPRECATED.md` → redirect to `react-lists`

### Quests to Promote (2 directories)

- [ ] **react-events**
  - Define minimal scope: onClick, onChange, preventDefault, event.target.value
  - Create refinement packet with deterministic tests
  - Add to `react_plus.json` (tier 2)

- [ ] **react-custom-hooks**
  - Define task: build `useToggle` or `useCounter` custom hook
  - Write tests using wrapper component pattern
  - Add to `react_plus.json` (tier 2)

### Quests to Hold (2 directories)

- [ ] **react-routing**
  - Check if assumes `react-router` dependency
  - If yes: park until deps policy decided
  - If stale: mark deprecated

- [ ] **react-performance-basics**
  - Evaluate if deterministic perf tests are feasible
  - Only promote if render count assertions can be controlled
  - Otherwise: keep as docs-only reference

---

## Suggested Audit Commands

```bash
# List all react directories
ls -la docs/quests | findstr react-

# Inspect each extra directory
for d in react-context react-custom-hooks react-effects react-events react-lists-keys react-performance-basics react-routing react-state; do
  echo "--- $d"
  ls -la "docs/quests/$d"
done

# Diff alias pairs
diff -ru docs/quests/react-effects docs/quests/react-effects-mount || true
diff -ru docs/quests/react-context docs/quests/react-context-theme || true
diff -ru docs/quests/react-state docs/quests/react-state-counter || true
diff -ru docs/quests/react-lists-keys docs/quests/react-lists || true
```

---

## Acceptance Criteria

- [x] Core pack (`react_core.json`) remains at 10 quests
- [x] Core quests fully scaffolded and verified (10/10 passing)
- [ ] Each extra dir has explicit decision recorded here
- [ ] Alias dirs contain `DEPRECATED.md` redirects
- [ ] No runner/questpack references point to extra dirs
- [ ] Optional: Create `react_plus.json` for promoted quests

---

## Related Files

- Questpack: [`data/questpacks/react_core.json`](file:///d:/EvalForge/data/questpacks/react_core.json)
- Test Runner: [`scripts/run_world_public_tests.mjs`](file:///d:/EvalForge/scripts/run_world_public_tests.mjs)
- Refinement Packets: [`react_refinement_packets.md`](file:///d:/EvalForge/react_refinement_packets.md)
