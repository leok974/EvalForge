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
        "technical_objective": "Write a script that defines a variable `status = 'ONLINE'` and prints it.",
        "rubric_hints": "Check for variable assignment and print."
    },
    {
        "id": "py_02", "track_id": "python-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "The Assembly Line",
        "technical_objective": "Create a list of 5 integers. Iterate through them and print each multiplied by 2.",
        "rubric_hints": "Check for list syntax and for loop."
    },
    {
        "id": "py_boss", "track_id": "python-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Automaton",
        "technical_objective": "Define a `Robot` class with an `__init__` method taking a name, and a `speak` method. Instantiate it.",
        "rubric_hints": "Check for class definition, __init__, self, and instantiation."
    },

    # --- JS WORLD (THE PRISM) ---
    {
        "id": "js_01", "track_id": "js-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Light Source",
        "technical_objective": "Write a JavaScript function `ignite()` that returns the string 'LASER ACTIVE'. Log the result.",
        "rubric_hints": "Check for function syntax and console.log."
    },
    {
        "id": "js_02", "track_id": "js-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "Refraction (Async)",
        "technical_objective": "Write an `async` function that awaits a 1-second timeout (simulated) and logs 'DONE'.",
        "rubric_hints": "Check for async/await keywords and setTimeout or Promise."
    },
    {
        "id": "js_boss", "track_id": "js-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: Data Transformation",
        "technical_objective": "Create a function that uses `.map()` to transform an array of numbers `[1,2,3]` into `[2,4,6]`.",
        "rubric_hints": "Check for Array.map usage and arrow functions."
    },

    # --- SQL WORLD (THE ARCHIVES) ---
    {
        "id": "sql_01", "track_id": "sql-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Retrieval",
        "technical_objective": "Write a SQL query to select `name` and `email` from a `users` table.",
        "rubric_hints": "Check for SELECT, FROM users."
    },
    {
        "id": "sql_02", "track_id": "sql-fundamentals", "sequence_order": 2, "tier": 1, "xp_reward": 100,
        "title": "The Filter",
        "technical_objective": "Write a query to find all users where `active = true` AND `role = 'admin'`.",
        "rubric_hints": "Check for WHERE clause and AND operator."
    },
    {
        "id": "sql_boss", "track_id": "sql-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Index",
        "technical_objective": "Write a query that performs an INNER JOIN between `users` and `orders` tables on `user_id`.",
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
        "title": "Container Launch",
        "technical_objective": "Write the `docker run` command to start a container named 'web' from image 'my-app' on port 8080.",
        "rubric_hints": "Check for docker run, -p 8080:80, --name."
    },
    {
        "id": "inf_boss", "track_id": "infra-fundamentals", "sequence_order": 3, "tier": 2, "xp_reward": 500,
        "title": "BOSS: The Circuit",
        "technical_objective": "Write a `docker-compose.yml` that defines two services: `web` and `db`.",
        "rubric_hints": "Check for version, services, and image keys."
    },

    # --- AGENTS WORLD (THE ORACLE) ---
    {
        "id": "ai_01", "track_id": "agent-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Invocation",
        "technical_objective": "Write a System Prompt that instructs an LLM to act as a 'Grumpy Pirate'.",
        "rubric_hints": "Check for persona definition and constraints."
    },
    {
        "id": "ai_boss", "track_id": "agent-fundamentals", "sequence_order": 2, "tier": 2, "xp_reward": 500,
        "title": "BOSS: Chain of Thought",
        "technical_objective": "Write a prompt that uses Few-Shot examples to teach an LLM how to convert JSON to SQL.",
        "rubric_hints": "Check for inclusion of examples (Input -> Output)."
    },

    # --- GIT WORLD (THE TIMELINE) ---
    {
        "id": "git_01", "track_id": "git-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Timeline Anchor",
        "technical_objective": "Initialize a new git repository and create the first commit with message 'Initial commit'.",
        "rubric_hints": "Check for git init, git add, git commit."
    },
    {
        "id": "git_boss", "track_id": "git-fundamentals", "sequence_order": 2, "tier": 2, "xp_reward": 300,
        "title": "BOSS: Timeline Divergence",
        "technical_objective": "Create a new branch named 'feature/login', switch to it, and push it to origin.",
        "rubric_hints": "Check for git checkout -b or git switch -c, and git push."
    },

    # --- ML WORLD (THE SYNAPSE) ---
    {
        "id": "ml_01", "track_id": "ml-fundamentals", "sequence_order": 1, "tier": 1, "xp_reward": 50,
        "title": "Neuron Activation",
        "technical_objective": "Using PyTorch, create a 2x2 Tensor of ones.",
        "rubric_hints": "Check for torch.ones((2,2))."
    },
    {
        "id": "ml_boss", "track_id": "ml-fundamentals", "sequence_order": 2, "tier": 2, "xp_reward": 500,
        "title": "BOSS: Matrix Multiplication",
        "technical_objective": "Perform a matrix multiplication between two 2x2 tensors A and B.",
        "rubric_hints": "Check for torch.matmul or @ operator."
    }
]

async def seed():
    print("📚 Populating The Archives (Curriculum)...")
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
