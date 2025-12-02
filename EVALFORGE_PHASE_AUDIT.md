# EvalForge Phase 22-34 Audit Report
**Date**: 2025-12-01  
**Status Legend**: ✅ Complete | ⚠️ Partial | ❌ Missing

---

## Phase 22 – Identity & Vanity (Avatars)

**Implementation**: ⚠️ Partial  
**Wiring**: ⚠️ Partial  
**UI**: ✅ Complete  
**Tests**: ❌ Missing

### Findings
- ✅ `User.current_avatar_id` field exists in models
- ❌ **`AvatarDefinition` model missing from `models.py`** (referenced in `seed_avatars.py` but not defined)
- ✅ Seed script exists: `scripts/seed_avatars.py` with 5 avatars
- ✅ Frontend components exist: `AvatarDisplay.tsx`, `AvatarSelector.tsx`
- ✅ Avatar visible in header (`CyberdeckLayout.tsx` line 42 - uses logo image)
- ⚠️ `/api/avatars` endpoints exist but return mock data (not DB-backed)

### TODOs
1. **CRITICAL**: Add `AvatarDefinition` model to `models.py` with fields: id, name, description, required_level, rarity, visual_type, visual_data
2. Update `/api/avatars` endpoint to query `AvatarDefinition` table instead of mock data
3. Add avatar component tests

---

## Phase 23 – Narrative Engine (World Lore)

**Implementation**: ✅ Complete  
**Wiring**: ⚠️ Partial  
**UI**: ✅ Complete  
**Tests**: ❌ Missing

### Findings
- ✅ All worlds in `data/worlds.json` have `narrative_config`:
  - alias (e.g. "THE FOUNDRY", "THE GRID")
  - theme
  - role
  - vocabulary
  - analogy_prompt
- ⚠️ Need to verify quest/explain helpers actually USE narrative_config in prompts

### TODOs
1. Verify `quest_helper.py` injects `narrative_config` into mission briefings
2. Verify `explain_helper.py` uses world theme for ELARA analogies
3. Add test that asserts vocabulary appears in generated prompts

---

## Phase 24 – NPC Upgrade (Personas)

**Implementation**: ✅ Complete  
**Wiring**: ✅ Complete  
**UI**: ✅ Complete  
**Tests**: ❌ Missing

### Findings
- ✅ `data/npcs.json` defines all 4 NPCs (KAI, ZERO, ELARA, PATCH) with complete metadata
- ✅ NPC chat headers visible in DevUI with name/title/color/icon
- ⚠️ Need to verify `persona_helper.py` exists and wraps prompts
- ⚠️ Need to verify agents emit `npc_identity` events

### TODOs
1. Verify `persona_helper.py` implements `get_npc()` and `wrap_prompt_with_persona()`
2. Verify agents (Quest/Judge/Explain/Debug) call persona wrapper
3. Add tests for persona wrapping

---

## Phase 25 – Tech Tree (Skill Nodes)

**Implementation**: ❌ Missing  
**Wiring**: ❌ Missing  
**UI**: ⚠️ Partial  
**Tests**: ❌ Missing

### Findings
- ❌ **`SkillNode` model MISSING from `models.py`**
- ❌ **`UserSkill` model MISSING**
- ❌ **`Profile.skill_points` field MISSING**
- ✅ `/api/skills` endpoint exists but returns empty/mock data
- ⚠️ Frontend `useSkills` hook exists and is used for gating
- ⚠️ `hasSkill()` checks exist in DevUI but always return false (no real data)

### TODOs
1. **CRITICAL**: Add models to `models.py`:
   - `SkillNode(id, name, description, cost, tier, category, feature_key, parent_id)`
   - `UserSkill(user_id, skill_id, unlocked_at)`
   - Add `skill_points: int` field to `Profile` model
2. **CRITICAL**: Create `scripts/seed_skills.py` with skill tree (syntax_highlighter, codex_link, agent_elara, agent_patch, etc.)
3. **CRITICAL**: Implement `skill_helper.py` with `unlock_skill()` logic (points check, dependency check)
4. Update `/api/skills` to return real data
5. Add `/api/skills/unlock` endpoint
6. Create TechTreeModal component (if not exists)
7. Add comprehensive skill tests

---

## Phase 26/30 – Codex (Great Library)

**Implementation**: ✅ Complete  
**Wiring**: ⚠️ Partial  
**UI**: ⚠️ Partial  
**Tests**: ❌ Missing

### Findings
- ✅ Codex directory structure exists: `data/codex/world-{python,js,agents,infra,evalforge}`
- ✅ Meta entries exist in `world-evalforge/` (KAI, ZERO, systems)
- ⚠️ Need to verify `codex_helper.py` exists with `load_codex_entry_by_id()`
- ⚠️ Need to verify ExplainAgent uses codex_id parameter
- ⚠️ Need to verify codex route exists in frontend (`/codex/:id`)

### TODOs
1. Verify `codex_helper.py` implementation
2. Verify ExplainAgent codex integration
3. Add codex route if missing
4. Add tests for codex loading and usage in explain prompts

---

## Phase 29/29b – Quest Engine & Curriculum

**Implementation**: ⚠️ Partial  
**Wiring**: ⚠️ Partial  
**UI**: ⚠️ Partial  
**Tests**: ❌ Missing

### Findings
- ✅ `QuestDefinition` model exists in `models.py`
- ⚠️ Need to verify `data/tracks.json` has fundamentals tracks for all worlds
- ⚠️ Need to verify `scripts/seed_curriculum.py` exists
- ⚠️ Need to verify `quest_helper.py` branches on fundamentals vs RAG

### TODOs
1. Verify `data/tracks.json` includes: python-fundamentals, js-fundamentals, sql-fundamentals, infra-fundamentals, agent-fundamentals, git-fundamentals, ml-fundamentals
2. Verify `scripts/seed_curriculum.py` exists and populates quests
3. Verify quest selection logic in `quest_helper.py`
4. Add tests for next quest selection

---

## Phase 31 – Registry / Project Ops

**Implementation**: ⚠️ Partial  
**Wiring**: ❌ Missing  
**UI**: ❌ Missing  
**Tests**: ❌ Missing

### Findings
- ⚠️ `arcade_app/tools.py` exists (need to verify project tools)
- ⚠️ Need to verify LangGraph integration
- ❌ Need to verify project-registry track exists

### TODOs
1. Verify tools.py has `list_my_projects`, `add_my_project`, `sync_my_project`
2. Verify `quest_agent_graph.py` exists with LangGraph
3. Add `project-registry` track to `data/tracks.json`
4. Add `data/codex/world-evalforge/system-registry.md`
5. Add tests for registry tool calls

---

## Phases 32-33b – Sensory Engine & FX

**Implementation**: ✅ Complete  
**Wiring**: ✅ Complete  
**UI**: ✅ Complete  
**Tests**: ❌ Missing

### Findings
- ✅ `useSound.ts` exists with theme assets
- ✅ `FXLayer.tsx` exists with layout-specific overlays
- ✅ `lib/fx.ts` FX Bus exists
- ✅ `ConfettiManager.tsx` exists
- ✅ `SettingsModal.tsx` has FX controls

### TODOs
1. Add tests for useSound theme selection
2. Add tests for FX event subscriptions

---

## Phase 34 – Boss Mechanics

**Implementation**: ⚠️ Partial  
**Wiring**: ⚠️ Partial  
**UI**: ✅ Complete  
**Tests**: ❌ Missing

### Findings
- ✅ `BossDefinition` model exists in `models.py`
- ✅ `BossRun` model exists
- ❌ **`BossProgress` model MISSING** (for fail streak tracking)
- ✅ `scripts/seed_bosses.py` exists
- ✅ Frontend: `BossHud.tsx`, `bossStore.ts`, `BossHistoryPanel.tsx` exist
- ⚠️ Need to verify `boss_progress_helper.py` exists
- ⚠️ Need to verify judge integration emits `boss_result` events
- ⚠️ Need to verify hint unlock flow

### TODOs
1. **CRITICAL**: Add `BossProgress` model to `models.py`:
   - Fields: user_id, boss_id, fail_count, hint_unlocked_at, hint_codex_id
2. **CRITICAL**: Create `boss_progress_helper.py` with `update_boss_progress()` logic
3. Verify judge calls progress helper after each boss run
4. Verify `boss_result` events include hint data
5. Verify BossHud "Strategy Guide" button works
6. Add boss strategy guides to `data/codex/world-evalforge/` (e.g. `boss-reactor-core.md`)
7. Add comprehensive boss tests

---

## Summary of Critical Gaps

### HIGH PRIORITY (Blocking Features)
1. **`AvatarDefinition` model missing** → Avatar system not DB-backed
2. **`SkillNode`/`UserSkill` models missing** → Skill tree completely non-functional
3. **`Profile.skill_points` missing** → No skill progression
4. **`BossProgress` model missing** → No fail streak / hint unlock system

### MEDIUM PRIORITY (Partial Features)
5. Skill tree implementation (`skill_helper.py`, `seed_skills.py`, unlock endpoint)
6. Boss progress helper and judge integration
7. Codex/ExplainAgent integration verification
8. Registry tools and LangGraph setup

### LOW PRIORITY (Testing / Polish)
9. Test coverage for all phases (currently 0% automated tests)
10. Verify narrative/persona integration in prompts
11. Codex route in frontend

---

## Recommended Next Steps

1. **Add Missing Models** (30 min)
   - `AvatarDefinition`, `SkillNode`, `UserSkill`, `BossProgress`
   - Update `Profile` with `skill_points`

2. **Implement Skill System** (2 hours)
   - `scripts/seed_skills.py`
   - `skill_helper.py` with unlock logic
   - `/api/skills/unlock` endpoint
   - Wire up to frontend

3. **Implement Boss Progress System** (1 hour)
   - `boss_progress_helper.py`
   - Judge integration
   - Boss strategy codex entries

4. **Add Critical Tests** (2 hours)
   - Skill unlock tests
   - Boss progress tests
   - Avatar selection tests
   - Codex integration tests

5. **Verify Integrations** (1 hour)
   - Persona helper usage in agents
   - Narrative config in quest prompts
   - Codex in ExplainAgent

**Total Estimated Effort**: 6-8 hours to achieve functional parity with design
