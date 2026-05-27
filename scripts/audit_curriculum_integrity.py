
import os
import json
import glob
import sys
import asyncio
import requests
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text
from sqlmodel import select

# Add root to pythonpath
sys.path.append(os.getcwd())
try:
    from arcade_app.models import QuestDefinition
    from arcade_app.config import DATABASE_URL
except ImportError:
    print("FATAL: Could not import EvalForge models or config. Run from project root.")
    sys.exit(1)

class CurriculumAuditor:
    def __init__(self, backend_url="http://localhost:8000"):
        self.backend_url = backend_url
        self.db_url = DATABASE_URL
        self.engine = create_async_engine(self.db_url)
        self.issues = []

    def log_issue(self, layer, quest_slug, message):
        self.issues.append({
            "layer": layer,
            "quest": quest_slug,
            "message": message
        })

    def audit_source_json(self):
        print("--- Layer A: Source JSON Audit ---")
        questpacks_path = os.path.join("data", "questpacks", "**", "*.json")
        files = glob.glob(questpacks_path, recursive=True)
        
        for f_path in files:
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                pack_name = os.path.basename(f_path)
                quests = []
                if isinstance(data, list): quests = data
                elif isinstance(data, dict):
                    if "quests" in data: quests = data["quests"]
                    elif "packs" in data: quests = data["packs"]

                for q in quests:
                    slug = q.get("slug") or q.get("id")
                    if not slug: continue
                    
                    if not q.get("short_description"):
                        # Check for legacy fields
                        legacy_fields = [f for f in ["description", "summary", "subtitle", "teaser", "blurb"] if q.get(f)]
                        if legacy_fields:
                            self.log_issue("SOURCE", slug, f"Missing short_description but has legacy fields: {legacy_fields}")
                        else:
                            self.log_issue("SOURCE", slug, "Missing short_description")
            except Exception as e:
                print(f"Error reading {f_path}: {e}")

    async def audit_database(self):
        print("--- Layer B: Database Audit ---")
        try:
            async with AsyncSession(self.engine) as session:
                stmt = select(QuestDefinition)
                results = (await session.exec(stmt)).all()
                print(f"Auditing {len(results)} quests in DB...")
                for q in results:
                    if not q.short_description:
                        self.log_issue("DATABASE", q.slug, "short_description is NULL or empty in DB")
        except Exception as e:
            print(f"Database error: {e}")

    async def audit_api(self):
        print("--- Layer C: API Audit ---")
        try:
            # We use the workshop catalog endpoint
            resp = requests.get(f"{self.backend_url}/api/workshop/quests", timeout=2)
            if resp.status_code != 200:
                print(f"API Error: {resp.status_code}")
                return

            data = resp.json()
            print(f"Auditing {len(data)} quests in API payload...")
            for q in data:
                slug = q.get("slug")
                if not q.get("short_description"):
                    self.log_issue("API", slug, "short_description missing from API payload")
        except Exception as e:
            print(f"API connection failed (is server running?): {e}")

    def report(self):
        print("\n=== CURRICULUM INTEGRITY REPORT ===")
        if not self.issues:
            print("No issues found! Curriculum is healthy.")
            return

        layers = {"SOURCE": [], "DATABASE": [], "API": []}
        for iss in self.issues:
            layers[iss["layer"]].append(iss)

        for layer, issues in layers.items():
            print(f"\n[{layer}] Layer Issues: {len(issues)}")
            # Show first 20
            for iss in issues[:20]:
                print(f"  - {iss['quest']}: {iss['message']}")
            if len(issues) > 20:
                print(f"  ... and {len(issues) - 20} more")

        # Summary for Snapshot
        summary = {
            "total_issues": len(self.issues),
            "by_layer": {l: len(issues) for l, issues in layers.items()}
        }
        with open("curriculum_integrity_report.json", "w") as f:
            json.dump(summary, f, indent=2)

async def main():
    auditor = CurriculumAuditor()
    auditor.audit_source_json()
    await auditor.audit_database()
    await auditor.audit_api()
    auditor.report()

if __name__ == "__main__":
    asyncio.run(main())
