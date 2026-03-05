import sys
import os
import json
import asyncio
from pathlib import Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

# Ensure we can import from arcade_app
sys.path.insert(0, os.path.abspath('.'))
from arcade_app.database import engine
from arcade_app.models import QuestDefinition

DOCS_DIR = Path("docs")
AUDITS_DIR = DOCS_DIR / "audits"
REPORT_PATH = AUDITS_DIR / "SEED_CONTENT_COMPLETENESS_REPORT.md"
BUDGET_PATH = AUDITS_DIR / "seed_content_budget.json"

async def audit_completeness():
    print("🔍 Auditing Seeded Quest Content Completeness...\n")
    
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load Budget
    budget = {"max_blocking_failures": 0, "max_debt_failures": 212}
    if BUDGET_PATH.exists():
        try:
            with open(BUDGET_PATH, "r") as f:
                budget = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load budget, using defaults: {e}")
            
    max_blocking = budget.get("max_blocking_failures", 0)
    max_debt = budget.get("max_debt_failures", 212)
    
    # Load Active Curriculum
    active_slugs = set()
    manifest_path = Path("data/seed/active_curriculum.json")
    if manifest_path.exists():
        try:
             with open(manifest_path, "r", encoding="utf-8") as f:
                 data = json.load(f)
             active_slugs = set(data.get("active_slugs", []))
        except Exception as e:
             print(f"⚠️ Failed to load active curriculum manifest: {e}")
    else:
         print(f"⚠️ Manifest not found at {manifest_path}, default to empty set.")
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    blocking_failures = []
    debt_failures = []
    
    async with async_session() as session:
        result = await session.execute(select(QuestDefinition))
        quests = result.scalars().all()
        
        print(f"Total Quests Scanned: {len(quests)}\n")
        
        for q in quests:
            issues = []
            
            # 1. Briefing
            has_briefing = bool(q.briefing_md and q.briefing_md.strip())
            has_detailed = bool(q.detailed_description and q.detailed_description.strip())
            if not has_briefing and not has_detailed:
                issues.append("Missing 'briefing_md' or equivalent description (Suggested: run objective backfill pipeline)")
                
            # 2. Starter Code
            has_starter = bool(q.starter_code and q.starter_code.strip())
            has_workspace = False
            if q.workspace_json and "files" in q.workspace_json:
                files = q.workspace_json["files"]
                # It's valid if there are files and at least one has content
                if any(f.get("content", "").strip() or f.get("path") for f in files):
                    has_workspace = True
                    
            if not has_starter and not has_workspace:
                issues.append("Missing 'starter_code' and empty 'workspace_json' (Suggested: re-seed from questpack)")
                
            # 3. Objectives
            if not q.objectives_json or len(q.objectives_json) == 0:
                issues.append("Empty 'objectives_json' (Suggested: run objective backfill pipeline)")
                
            # 4. Key Terms (>= 3 for Tier 2)
            is_tier_2 = "-t2-" in q.slug or "_t2_" in q.slug or "Tier 2" in q.title or "(T2)" in q.title
            if is_tier_2:
                terms_count = len(q.key_terms) if q.key_terms else 0
                if terms_count < 3:
                    issues.append(f"Insufficient 'key_terms' for Tier 2 (found {terms_count}, need 3+) (Suggested: add Codex terms)")
                    
            if issues:
                failure_record = {
                    "slug": q.slug,
                    "title": q.title,
                    "issues": issues
                }
                
                # Determine classification
                is_blocking = q.slug in active_slugs
                if is_blocking:
                    blocking_failures.append(failure_record)
                else:
                    debt_failures.append(failure_record)

    # Generate Report
    report_lines = [
        "# Seed Content Completeness Report\n",
        f"Total quests scanned: {len(quests)}\n",
        f"## Blocking Failures ({len(blocking_failures)} / {max_blocking} allowed)\n",
        "These are quests in the active curriculum (data/questpacks) or Tier 2 strict quests.\n"
    ]
    
    if not blocking_failures:
        report_lines.append("✅ No blocking failures.\n")
    else:
        for fq in blocking_failures:
            report_lines.append(f"### {fq['title']} (`{fq['slug']}`)")
            for issue in fq["issues"]:
                report_lines.append(f"- {issue}")
            report_lines.append("")
            
    report_lines.append(f"\n## Debt Failures ({len(debt_failures)} / {max_debt} allowed)\n")
    report_lines.append("These are legacy/historical quests waiting for backfill.\n")
    
    if not debt_failures:
        report_lines.append("✅ No debt failures.\n")
    else:
        for fq in debt_failures:
            report_lines.append(f"### {fq['title']} (`{fq['slug']}`)")
            for issue in fq["issues"]:
                report_lines.append(f"- {issue}")
            report_lines.append("")

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    
    print(f"Report written to: {REPORT_PATH}")
    print(f"SeedContent blocking={len(blocking_failures)} debt={len(debt_failures)} budget_debt={max_debt}")
    
    passed = True
    if len(blocking_failures) > max_blocking:
        print(f"❌ Audit Failed. Blocking failures ({len(blocking_failures)}) exceed budget ({max_blocking}).")
        passed = False
    if len(debt_failures) > max_debt:
        print(f"❌ Audit Failed. Debt failures ({len(debt_failures)}) exceed budget ({max_debt}).")
        passed = False
        
    if passed:
        print("✅ Audit Passed.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(audit_completeness())
