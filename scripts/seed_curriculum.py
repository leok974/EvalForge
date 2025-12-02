import asyncio
import sys
import os

# Ensure we can import from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arcade_app.database import init_db, get_session
from arcade_app.models import QuestDefinition

FULL_CURRICULUM = [
    # --- PYTHON WORLD (THE FOUNDRY) ---
    {
        "id": "py_01", "track_id": "python-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Ignition",
        "technical_objective": "Define a variable `status = 'ONLINE'` and print it.",
        "rubric_hints": "Check for variable assignment and print."
    },
    {
        "id": "py_02", "track_id": "python-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "The Loop",
        "technical_objective": "Create a list of 5 integers and print each multiplied by 2.",
        "rubric_hints": "Check for list and for loop."
    },
    {
        "id": "py_03", "track_id": "python-fundamentals", "sequence_order": 3, "tier": 1, "xp_reward": 150,
        "title": "Data Forge",
        "technical_objective": "Use a dictionary to map 3 status codes to messages and print them.",
        "rubric_hints": "Check for dict literal and iteration."
    },
    {
        "id": "py_boss", "track_id": "python-fundamentals", "sequence_order": 4, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Automaton",
        "technical_objective": "Define a Robot class with __init__(name) and speak(); instantiate and call speak().",
        "rubric_hints": "Check for class definition, __init__, self, and instantiation."
    },

    # --- JS WORLD (THE PRISM) ---
    {
        "id": "js_01", "track_id": "js-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Light Source",
        "technical_objective": "Write a JavaScript function `ignite()` that returns the string 'LASER ACTIVE' and log the result.",
        "rubric_hints": "Check for function syntax and console.log."
    },
    {
        "id": "js_02", "track_id": "js-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "Refraction (Async)",
        "technical_objective": "Write an `async` function that awaits a 1-second timeout and logs 'DONE'.",
        "rubric_hints": "Check for async/await and Promise/timeout usage."
    },
    {
        "id": "js_boss", "track_id": "js-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Event Loop",
        "technical_objective": "Create a function that uses `.map()` to transform `[1,2,3]` into `[2,4,6]`, and log the result.",
        "rubric_hints": "Check for Array.map and arrow function."
    },

    # --- SQL WORLD (THE ARCHIVES) ---
    {
        "id": "sql_01", "track_id": "sql-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Retrieval",
        "technical_objective": "Write a SQL query to select `name` and `email` from a `users` table.",
        "rubric_hints": "Check for SELECT and FROM users."
    },
    {
        "id": "sql_02", "track_id": "sql-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "The Filter",
        "technical_objective": "Write a query to find all users where `active = true` AND `role = 'admin'`.",
        "rubric_hints": "Check for WHERE clause with AND."
    },
    {
        "id": "sql_boss", "track_id": "sql-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Index",
        "technical_objective": "Write a query that performs an INNER JOIN between `users` and `orders` on `users.id = orders.user_id`.",
        "rubric_hints": "Check for INNER JOIN syntax and ON condition."
    },

    # --- INFRA WORLD (THE GRID) ---
    {
        "id": "inf_01", "track_id": "infra-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Containment Field",
        "technical_objective": "Write a simple `Dockerfile` for a Python application using `python:3.9-slim`.",
        "rubric_hints": "Check for FROM, WORKDIR, COPY, and CMD."
    },
    {
        "id": "inf_02", "track_id": "infra-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "Service Link",
        "technical_objective": "Write a `docker-compose.yml` that defines two services: `web` and `db`.",
        "rubric_hints": "Check for services, web, and db keys."
    },
    {
        "id": "inf_boss", "track_id": "infra-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Circuit",
        "technical_objective": "Write a `docker-compose.yml` that connects `web` and `db` on a custom network and sets environment variables.",
        "rubric_hints": "Check for networks, environment, and depends_on."
    },

    # --- AGENTS WORLD (THE ORACLE) ---
    {
        "id": "ai_01", "track_id": "agent-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Invocation",
        "technical_objective": "Write a system prompt that instructs an LLM to act as a 'Grumpy Pirate' with clear behavioral rules.",
        "rubric_hints": "Check for persona description, constraints, and forbidden behaviors."
    },
    {
        "id": "ai_02", "track_id": "agent-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "Grounding",
        "technical_objective": "Write a prompt that instructs the LLM to answer only using provided context (RAG style).",
        "rubric_hints": "Check for context placeholders and 'do not hallucinate' instructions."
    },
    {
        "id": "ai_boss", "track_id": "agent-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: Chain of Thought",
        "technical_objective": "Write a prompt that uses 2–3 input/output examples to teach an LLM how to convert simple JSON records into SQL INSERT statements.",
        "rubric_hints": "Check for few-shot examples, clear task description, and output format constraints."
    },

    # --- GIT WORLD (THE TIMELINE) ---
    {
        "id": "git_01", "track_id": "git-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Commit Protocol",
        "technical_objective": "Write the exact Git commands to initialize a repo, stage a file, and commit it.",
        "rubric_hints": "Check for git init, git add, and git commit."
    },
    {
        "id": "git_02", "track_id": "git-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "Branch Divergence",
        "technical_objective": "Write the commands to create a new branch `feature/ui` and switch to it.",
        "rubric_hints": "Check for git branch/checkout -b/switch."
    },
    {
        "id": "git_boss", "track_id": "git-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: Rebase Ritual",
        "technical_objective": "Explain and show commands to rebase a feature branch onto main.",
        "rubric_hints": "Check for git rebase main and conflict resolution awareness."
    },

    # --- ML WORLD (THE SYNAPSE) ---
    {
        "id": "ml_01", "track_id": "ml-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Tensor Warmup",
        "technical_objective": "Using PyTorch, create a 1D tensor of values [1, 2, 3] and compute its mean.",
        "rubric_hints": "Check for `torch.tensor` and `tensor.mean()`."
    },
    {
        "id": "ml_02", "track_id": "ml-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "Gradient Flow",
        "technical_objective": "Write a minimal training step that performs a forward pass, computes MSE loss, calls `backward()`, and steps an optimizer.",
        "rubric_hints": "Check for model(inputs), loss, loss.backward(), optimizer.step(), optimizer.zero_grad()."
    },
    {
        "id": "ml_boss", "track_id": "ml-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: Tiny Network",
        "technical_objective": "Describe and implement code to intentionally overfit a tiny dataset and log train vs validation loss.",
        "rubric_hints": "Check for tiny dataset, multiple epochs, training loop, and printed/logged losses for both splits."
    }
]

async def seed():
    print("📚 Populating The Archives (Curriculum)...")
    
    # Debug: Check registered tables
    from sqlmodel import SQLModel
    print(f"Registered Tables: {list(SQLModel.metadata.tables.keys())}")
    
    await init_db()
    async for session in get_session():
        # Clear existing data to avoid Unique Constraint violations
        # Note: This resets progress!
        from sqlalchemy import text
        await session.execute(text("DELETE FROM userquest"))
        await session.execute(text("DELETE FROM questdefinition"))
        
        count = 0
        for data in FULL_CURRICULUM:
            # Upsert logic
            q = QuestDefinition(**data)
            await session.merge(q)
            count += 1
        await session.commit()
    print(f"✅ Loaded {count} Quests across 7 Worlds.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())
