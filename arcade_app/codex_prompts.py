"""
LLM Prompt Templates for Project Codex Doc Generation.

Each doc_type has a specialized prompt template that guides the LLM
to generate structured, consistent documentation with YAML frontmatter.
"""

# System prompt used for all doc generation
SYSTEM_PROMPT = """You are a technical documentation expert for EvalForge, an AI-powered learning platform.

Your task: Generate structured Project Codex documentation from repository files.

**Output Requirements:**
1. Start with YAML frontmatter (between --- markers)
2. Follow with clear, technical Markdown content
3. Use ## headings for main sections
4. Be concise but informative
5. Focus on architecture and technical decisions, not marketing

**YAML Frontmatter Fields:**
- project: {project_slug}
- doc_type: {doc_type}
- worlds: [world-python, world-sql, world-infra, world-agents, etc.]
- level: 1-5 (difficulty/complexity tier)
- stack: nested dict of frontend/backend/storage/infra
- domains: [problem domain keywords]
- tags: [technology tags like fastapi, react, postgres]

**Tone:** Technical but accessible. Write for developers who want to understand the system quickly."""


def get_overview_prompt(project_slug: str, snippets: str, scan_meta: dict) -> str:
    """Prompt for generating Project Overview documentation."""
    return f"""Generate a Project Codex **Overview** document for the project "{project_slug}".

**Available Context:**
{snippets}

**Detected Stack:** {', '.join(scan_meta.get('stack', []))}
**Languages:** {', '.join(scan_meta.get('languages', {}).keys())}
**Worlds:** {', '.join(scan_meta.get('worlds', []))}

**Required Sections:**
## Mission
1-2 paragraphs: What problem does this solve? Who uses it? What need does it address?

## Core Features
Bullet list of 5-7 main features or capabilities

## Tech Stack (High Level)
- **Frontend:** (framework, styling, build tool)
- **Backend:** (API framework, language)
- **Storage:** (databases, caches, search engines)
- **Infra:** (deployment, containers, CI/CD)
- **AI/ML:** (if applicable: LLMs, agents, embeddings)

## Worlds & Skills (EvalForge Mapping)
Map this project to relevant EvalForge worlds and explain what skills each world covers:
- **Python / Backend (The Foundry):** What backend code exists?
- **SQL / Data (The Archives):** What data models or queries?  
- **Infra / DevOps (The Grid):** What deployment setup?
- **Agents (The Oracle):** Any AI agents or LLM tools?
- **Git / Process (The Timeline):** Any interesting workflows?

## Current Maturity
- Stage: (prototype / beta / production-ready)
- Test coverage: (rough assessment)
- Observability: (metrics, logging, monitoring status)

**Output the complete frontmatter + markdown document.**"""


def get_architecture_prompt(project_slug: str, snippets: str, scan_meta: dict) -> str:
    """Prompt for generating Architecture documentation."""
    return f"""Generate a Project Codex **Architecture** document for "{project_slug}".

**Available Context:**
{snippets}

**Services Detected:** {', '.join([s['name'] for s in scan_meta.get('services', [])])}
**Stack:** {', '.join(scan_meta.get('stack', []))}

- **EntityName:** Purpose and key fields

## Relationships
Describe important relationships between entities:
- One-to-many, many-to-many patterns
- Foreign keys and constraints

## Indices & Performance
- Important indices for query performance
- Any materialized views or denormalization

## Data Lifecycle
- How data is created, updated, archived
- Retention policies if any

**Output the complete frontmatter + markdown document.**"""


def get_data_model_prompt(project_slug: str, snippets: str, scan_meta: dict) -> str:
    """Prompt for generating Data Model documentation."""
    return f"""Generate a Project Codex **Data Model** document for "{project_slug}".

**Available Context:**
{snippets}

**Required Sections:**
## Overview
Brief description of the data architecture approach

## Key Entities
List 5-10 main entities/tables with:
- **EntityName:** Purpose and key fields

## Relationships
Describe important relationships between entities:
- One-to-many, many-to-many patterns
- Foreign keys and constraints

## Indices & Performance
- Important indices for query performance
- Any materialized views or denormalization

## Data Lifecycle
- How data is created, updated, archived
- Retention policies if any

**Output the complete frontmatter + markdown document.**"""


def get_infra_prompt(project_slug: str, snippets: str, scan_meta: dict) -> str:
    """Prompt for generating Infrastructure documentation."""
    return f"""Generate a Project Codex **Infra** document for "{project_slug}".

**Available Context:**
{snippets}

**Required Sections:**
## Overview
High-level infrastructure approach (containers, cloud, on-prem, etc.)

## Local Development
- How to run locally
- Required environment variables
- Common commands (start, test, migrate)

## Production Deployment
- Deployment method (Docker Compose, K8s, serverless, etc.)
- Key services and their ports/endpoints
- Health checks and readiness probes

## Environment Variables
List critical env vars and their purposes

## Networking
- How services communicate
- External integrations (APIs, webhooks)

## Scaling Considerations
- What's stateless vs stateful
- How to scale horizontally

**Output the complete frontmatter + markdown document.**"""


def get_agents_prompt(project_slug: str, snippets: str, scan_meta: dict) -> str:
    """Prompt for generating Agents documentation."""
    return f"""Generate a Project Codex **Agents** document for "{project_slug}".

**Available Context:**
{snippets}

**Required Sections:**
## Overview
What agentic or AI-powered components exist in this project?

## Agent Definitions
For each agent/tool:
- **AgentName:** Purpose and capabilities
- **Inputs:** What it consumes
- **Outputs:** What it produces
- **LLM/Model:** What model it uses (if any)

## Tool Ecosystem
List available tools and their functions

## Safety & Guardrails
- How agents are constrained
- Human-in-the-loop checkpoints
- Rollback mechanisms

## Future Enhancements
Planned agent improvements or new agents

**Output the complete frontmatter + markdown document.**"""


def get_quest_hooks_prompt(project_slug: str, snippets: str, scan_meta: dict) -> str:
    """Prompt for generating Quest Hooks documentation."""
    return f"""Generate a Project Codex **Quest Hooks** document for "{project_slug}".

**Available Context:**
{snippets}

This document suggests learning opportunities and challenges within this codebase.

**Required Sections:**
## Good Practice Quests
Suggest 3-5 small, well-scoped tasks suitable for learning:
1. **Quest Name**  
   Description: What to build/fix and why it matters  
   Difficulty: 1-3 (beginner to intermediate)

## Boss Fights
Suggest 1-2 complex challenges requiring deep system understanding:
1. **Boss Name**  
   - **Objective:** What needs to be accomplished
   - **Constraints:** Rules or requirements
   - **Skills Tested:** What worlds/skills this exercises
   - **Difficulty:** 4-5 (advanced)

Include ideas from TODOs, roadmap items, or areas that could use improvement.

**Output the complete frontmatter + markdown document with quest_ideas and boss_ideas in frontmatter.**"""


# Map doc_type to prompt function
PROMPT_GENERATORS = {
    "overview": get_overview_prompt,
    "architecture": get_architecture_prompt,
    "data_model": get_data_model_prompt,
    "infra": get_infra_prompt,
    "agents": get_agents_prompt,
    "quest_hooks": get_quest_hooks_prompt,
}


def get_prompt_for_doc_type(doc_type: str, project_slug: str, snippets: str, scan_meta: dict) -> str:
    """
    Get the full prompt for a specific doc_type.
    
    Args:
        doc_type: Type of documentation to generate
        project_slug: Project identifier
        snippets: Combined file snippets from CandidateSelector
        scan_meta: Metadata from RepoScanner
        
    Returns:
        Complete prompt string to send to LLM
    """
    prompt_fn = PROMPT_GENERATORS.get(doc_type)
    if not prompt_fn:
        raise ValueError(f"Unknown doc_type: {doc_type}")
    
    return prompt_fn(project_slug, snippets, scan_meta)
