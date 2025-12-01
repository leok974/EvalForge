import os

META_DOCS = {
    "entity-kai": """---
id: entity-kai
title: KAI (Quest Protocol)
world: world-evalforge
tier: 1
tags: [meta, npc, agents]
summary: The Tactical Operator responsible for mission assignment.
source: curated
---

# Identity Profile
> **Designation:** KAI (Kernel Access Interface)
> **Role:** Mission Control / Quest Giver
> **Voice:** Tactical, Urgent, Military-Industrial.

KAI is the first voice you hear. He monitors the stability of The Grid and assigns **Missions** to Architects to repair entropy (bugs). He values precision and speed.

# Technical Specifications (Serious Mode)
Under the hood, KAI is the **QuestAgent** (`arcade_app.agent.QuestAgent`).
- **Fundamentals:** Reads from `QuestDefinition` SQL table for linear progression using `quest_helper.py`.
- **Field Ops:** Uses RAG to scan your `projects.json` repos, identifies potential refactors, and generates dynamic tickets via Gemini 2.5.
- **Personality:** Injected via `persona_helper.py` using `data/npcs.json`.
""",

    "entity-zero": """---
id: entity-zero
title: ZERO (System Arbiter)
world: world-evalforge
tier: 1
tags: [meta, npc, agents]
summary: The cold logic core that evaluates all submissions.
source: curated
---

# Identity Profile
> **Designation:** ZERO
> **Role:** The Judge / Compliance Officer
> **Voice:** Cold, Binary, Terrifyingly Logical.

ZERO is the immune system of The Construct. He ensures all code submissions meet the strict architectural standards of reality. Failure to comply results in immediate rejection.

# Technical Specifications
ZERO is the **JudgeAgent**.
- **Grading:** Uses `grading_helper.py` to evaluate code against a rubric (Correctness, Coverage, Clarity).
- **Gamification:** Triggers `add_xp` and `process_quest_completion` upon passing scores.
- **Strict Mode:** If `EVALFORGE_MOCK_GRADING=0`, ZERO uses Vertex AI to perform AST analysis and unit testing logic.
""",

    "entity-elara": """---
id: entity-elara
title: ELARA (The Archivist)
world: world-evalforge
tier: 2
tags: [meta, npc, agents]
summary: The keeper of the Codex and ancient wisdom.
source: curated
---

# Identity Profile
> **Designation:** ELARA (Elder Logic Archival Routine)
> **Role:** Mentor / Teacher
> **Voice:** Wise, Patient, Mystical.

ELARA guards the **Codex**. She guides Architects through the complexity of the system, offering explanations and historical context rather than direct answers.

# Technical Specifications
ELARA is the **ExplainAgent**, powered by **LangGraph**.
- **Reasoning:** Uses a ReAct loop (`graph_agent.py`) to decide when to consult documentation.
- **Tools:** Calls `retrieve_docs` to perform Vector Search on the Codex.
- **Context:** Aware of the current World/Track and injects stack-specific examples.
""",

    "entity-patch": """---
id: entity-patch
title: PATCH (Glitch Hunter)
world: world-evalforge
tier: 3
tags: [meta, npc, agents]
summary: The cynical engineer who fixes what others break.
source: curated
---

# Identity Profile
> **Designation:** PATCH
> **Role:** Debugger / Mechanic
> **Voice:** Gritty, Cynical, Hands-on.

PATCH has seen every error code in existence. He doesn't care about "clean code"; he cares about code that *works*. He lives in the error logs.

# Technical Specifications
PATCH is the **DebugAgent**.
- **Capabilities:** Specialized in reading stack traces and diffing code.
- **RAG Access:** Has deep access to the `repo_scanner` index to find definitions across files.
- **Constraints:** Only unlocked after Tier 3 in the Tech Tree.
""",

    "system-cybernetics": """---
id: system-cybernetics
title: Cybernetics (Skill Tree)
world: world-evalforge
tier: 1
tags: [meta, system, progression]
summary: Neural augmentations that unlock new capabilities.
source: curated
---

# System Overview
The **Cybernetics Lab** allows Architects to upgrade their interface. By spending Skill Points (SP) earned from leveling up, you can unlock new modules.

# Technical Specifications
- **Data Model:** `SkillNode` and `UserSkill` in Postgres.
- **Logic:** `skill_helper.py` validates dependencies (Parent/Child) and cost.
- **Frontend:** `useSkills` hook gates UI features (e.g. disabling the "Explain" button if `module_elara` is locked).
""",

    "system-ingestion": """---
id: system-ingestion
title: Project Ingestion (The Bridge)
world: world-evalforge
tier: 2
tags: [meta, system, rag]
summary: The mechanism for assimilating external codebases.
source: curated
---

# System Overview
**The Bridge** connects The Construct to external Git repositories. It scans, maps, and indexes code so Agents can understand your personal projects.

# Technical Specifications
- **Worker:** `ingestion_helper.py` runs in a background thread/worker.
- **Clone:** Uses `GitPython` to shallow clone repos to temp dirs.
- **Map:** Generates a virtual `PROJECT_MAP.md` tree structure.
- **Vector:** Chunks files and embeds them using `text-embedding-004` into `pgvector`.
- **Events:** Broadcasts progress via Redis Pub/Sub (`sync_progress`).
""",

    "system-cyberdeck": """---
id: system-cyberdeck
title: The Cyberdeck (Interface)
world: world-evalforge
tier: 1
tags: [meta, system, ui]
summary: The primary visual interface for the Architect.
source: curated
---

# System Overview
The **Cyberdeck** is your HUD. It aggregates telemetry, communication, and code editing into a unified view.

# Technical Specifications
- **Stack:** React + Tailwind + Framer Motion.
- **Real-Time:** Uses `useArcadeStream` (SSE) for chat and `useGameSocket` (WebSockets) for events.
- **Theming:** Supports multiple Layouts (`Cyberdeck`, `Navigator`, `Workshop`) via `GameShell`.
"""
}

def seed():
    print("🌌 Seeding The Construct (Meta-Docs)...")
    base_dir = "data/codex/world-evalforge"
    os.makedirs(base_dir, exist_ok=True)
    
    for filename, content in META_DOCS.items():
        path = os.path.join(base_dir, f"{filename}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   + Wrote {filename}.md")
        
    print("✅ The Architect's Manual is online.")

if __name__ == "__main__":
    seed()
