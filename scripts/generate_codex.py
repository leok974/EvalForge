import os
import sys
import argparse
import asyncio
import re
import json

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "291179078777")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL_NAME = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.0-flash-exp")

TEMPLATE = """---
id: {slug}
title: {title}
world: {world}
tier: {tier}
difficulty: {difficulty}
tags: [{tags}]
summary: >-
  {summary}
version: 1
last_updated: 2025-11-29
xp_reward: {xp}
prerequisites: []
stack: []
source: llm-draft
trust_level: draft
---

# Definition
> TL;DR: {tldr}

# The Golden Path (Best Practice)
{golden_path}

# Common Pitfalls (Anti-Patterns)
{anti_patterns}

# Trade-offs
{trade_offs}

# Deep Dive (Internals)
{deep_dive}

# Interview Questions
{interview_questions}
"""

TIER_CONFIG = {
    1: {"diff": "beginner", "xp": 50, "len": "Keep it concise (400-700 words). Focus on syntax and basic usage."},
    2: {"diff": "intermediate", "xp": 100, "len": "Detailed (800-1200 words). Focus on patterns and standard practices."},
    3: {"diff": "advanced", "xp": 200, "len": "Deep Dive (1200+ words). Focus on architecture, internals, and tricky edge cases."}
}

async def generate_draft(topic: str, world: str, tier: int):
    print(f"✍️  Auto-Scribing Tier {tier} draft for: '{topic}' in {world}...")
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_NAME)
    
    config = TIER_CONFIG.get(tier, TIER_CONFIG[2])
    
    prompt = f"""
    ROLE: Senior Staff Engineer writing internal documentation.
    TASK: Write a Tier {tier} ({config['diff']}) technical guide about "{topic}" for "{world}".
    LENGTH_GUIDELINE: {config['len']}
    
    REQUIREMENTS:
    1. Structure: Follow the strict JSON format below.
    2. Tone: Professional, opinionated, "Best Practice" focused.
    3. Stack Context: Assume the reader uses the specific stack for {world} (e.g. Python=FastAPI/SQLModel).
    4. Code: Provide realistic, copy-pasteable snippets.
    
    OUTPUT FORMAT (JSON):
    {{
        "slug": "kebab-case-slug",
        "title": "Clear Technical Title",
        "tags": "tag1, tag2",
        "summary": "One sentence summary.",
        "tldr": "The absolute core concept in one line.",
        "golden_path": "Markdown content for best practice.",
        "anti_patterns": "Markdown content for what NOT to do.",
        "trade_offs": "- ✅ Pro\\n- ❌ Con",
        "deep_dive": "Markdown explaining internals.",
        "interview_questions": "1. Q?\\n2. Q?"
    }}
    """
    
    response = await model.generate_content_async(prompt, generation_config={"response_mime_type": "application/json"})
    data = re.sub(r"```json\n|\n```", "", response.text).strip()
    
    try:
        content = json.loads(data)
        # print(f"DEBUG: Type: {type(content)}")
        
        while isinstance(content, list):
            print("⚠️  Warning: Model returned a list. Using first item.")
            if not content:
                raise ValueError("Empty list returned")
            content = content[0]
            
        if not isinstance(content, dict):
             raise ValueError(f"Expected dict, got {type(content)}")
             
    except Exception as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"Raw Output: {response.text}")
        return

    final_md = TEMPLATE.format(
        slug=content.get('slug', 'unknown-slug'),
        title=content.get('title', 'Untitled'),
        world=world,
        tier=tier,
        difficulty=config['diff'],
        tags=content.get('tags', ''),
        xp=config['xp'],
        summary=content.get('summary', ''),
        tldr=content.get('tldr', ''),
        golden_path=content.get('golden_path', ''),
        anti_patterns=content.get('anti_patterns', ''),
        trade_offs=content.get('trade_offs', ''),
        deep_dive=content.get('deep_dive', ''),
        interview_questions=content.get('interview_questions', '')
    )
    
    output_dir = f"data/codex/{world}"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{content.get('slug', 'unknown')}_draft.md")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(final_md)
        
    print(f"✅ Saved: {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("topics", nargs="+")
    parser.add_argument("--world", required=True)
    parser.add_argument("--tier", type=int, default=2)
    
    args = parser.parse_args()
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    async def main():
        for topic in args.topics:
            await generate_draft(topic, args.world, args.tier)
            
    asyncio.run(main())
