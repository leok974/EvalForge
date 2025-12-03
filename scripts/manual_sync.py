import asyncio
import os
import sys
import tempfile
import shutil
from sqlmodel import select

# Add project root to path
sys.path.append(os.getcwd())

from arcade_app.database import get_session
from arcade_app.models import Project, User, ProjectCodexDoc
from arcade_app.codex_scanner import RepoScanner
from arcade_app.codex_candidate_selector import CandidateSelector
from arcade_app.codex_generator import CodexDocGenerator

async def main():
    print("Starting manual sync for 'applylens' (using dummy files)...")
    
    # Create a temporary directory with dummy project files
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📂 Created temp dir: {temp_dir}")
        
        # Create README.md
        with open(os.path.join(temp_dir, "README.md"), "w") as f:
            f.write("""# ApplyLens
ApplyLens is an AI-powered job application tracker.
It helps users track their applications, analyze job descriptions, and tailor their resumes.

## Tech Stack
- Frontend: React, Tailwind
- Backend: FastAPI, Python 3.11
- Database: PostgreSQL
- AI: Vertex AI (Gemini)
""")

        # Create ARCHITECTURE.md
        with open(os.path.join(temp_dir, "ARCHITECTURE.md"), "w") as f:
            f.write("""# Architecture
The system consists of a React frontend and a FastAPI backend.
Data is stored in Postgres.
We use Celery for background tasks.
""")

        # Create main.py
        with open(os.path.join(temp_dir, "main.py"), "w") as f:
            f.write("""from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
""")

        # Create an agent file
        os.makedirs(os.path.join(temp_dir, "agents"), exist_ok=True)
        with open(os.path.join(temp_dir, "agents", "job_agent.py"), "w") as f:
            f.write("""class JobAgent:
    def analyze(self, job_desc):
        # Use LLM to analyze
        pass
""")

        repo_path = temp_dir
        
        async for session in get_session():
            # Find or Create Project
            stmt = select(Project).where(Project.name == "ApplyLens")
            result = await session.execute(stmt)
            project = result.scalar_one_or_none()
            
            if not project:
                print("Project 'ApplyLens' not found. Creating it...")
                # Create dummy user if needed
                user_stmt = select(User).where(User.id == "user_1")
                user_result = await session.execute(user_stmt)
                user = user_result.scalar_one_or_none()
                if not user:
                    user = User(id="user_1", name="Test User")
                    session.add(user)
                    await session.commit()
                
                project = Project(
                    name="ApplyLens",
                    repo_url="https://github.com/example/applylens",
                    owner_user_id="user_1",
                    default_world_id="world-python",
                    summary_data={"stack": ["fastapi", "react"]}
                )
                session.add(project)
                await session.commit()
                await session.refresh(project)
                print(f"Created project {project.id}")

            try:
                print(f"🔍 Starting Codex Analysis for {project.name}...")
                
                # Initialize pipeline components
                scanner = RepoScanner()
                selector = CandidateSelector()
                generator = CodexDocGenerator()
                
                # Stage 1: Scan
                scan_results = scanner.scan(repo_path)
                print(f"📊 Scan complete. Found {len(scan_results.get('core_docs', {}))} core docs.")
                
                # Doc types to generate
                doc_types = ["overview", "architecture", "agents"]
                
                for doc_type in doc_types:
                    # Stage 2: Select Candidates
                    candidates = selector.select_candidates(repo_path, doc_type, scan_results)
                    print(f"  - {doc_type}: Found {len(candidates)} candidates")
                    
                    if candidates:
                        # Stage 3: Generate
                        print(f"  - Generating {doc_type} doc...")
                        
                        doc_data = await generator.generate_doc(
                            project_slug=project.name.lower().replace(" ", "-"),
                            doc_type=doc_type,
                            file_snippets=candidates,
                            scan_meta=scan_results
                        )
                        
                        print(f"    > Generated Title: {doc_data['title']}")
                        print(f"    > Generated Body Length: {len(doc_data['body_md'])}")
                        print(f"    > Frontmatter Check: {'---' in doc_data['body_md'][:10]}")
                        
                        # Stage 4: Upsert
                        stmt = select(ProjectCodexDoc).where(
                            ProjectCodexDoc.project_id == project.id,
                            ProjectCodexDoc.doc_type == doc_type
                        )
                        result = await session.execute(stmt)
                        existing_doc = result.scalar_one_or_none()
                        
                        if existing_doc:
                            if not existing_doc.auto_generated:
                                print(f"    Skipping {doc_type} (manually edited)")
                                continue
                            
                            existing_doc.title = doc_data["title"]
                            existing_doc.summary = doc_data["summary"]
                            existing_doc.body_md = doc_data["body_md"]
                            existing_doc.world_ids = doc_data["world_ids"]
                            existing_doc.tags = doc_data["tags"]
                            from datetime import datetime
                            existing_doc.updated_at = datetime.utcnow()
                            session.add(existing_doc)
                            print(f"    Updated {doc_type}")
                        else:
                            new_doc = ProjectCodexDoc(
                                project_id=project.id,
                                doc_type=doc_type,
                                **doc_data
                            )
                            session.add(new_doc)
                            print(f"    Created {doc_type}")
                        
                        await session.commit()
                
                # Update Project Status
                project.codex_status = "complete"
                session.add(project)
                await session.commit()
                
                print("Sync completed successfully!")
                
            except Exception as e:
                print(f"Sync failed: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
