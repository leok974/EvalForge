import os
import shutil
import tempfile
import git
import json
import time
from datetime import datetime
from typing import List, Dict
from redis.asyncio import Redis
from sqlmodel import select
from arcade_app.rag_helper import index_content
from arcade_app.database import get_session
from arcade_app.models import Project, ProjectCodexDoc
from arcade_app.codex_scanner import RepoScanner
from arcade_app.codex_candidate_selector import CandidateSelector
from arcade_app.codex_generator import CodexDocGenerator

# Redis Config (match your docker-compose/env)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6380/0")

# File extensions we care about for code analysis
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".json", ".sql", ".yml", ".yaml",
    ".dockerignore", ".gitignore"
}

# Directories to strictly ignore
IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", "venv", "env", "dist", "build", ".next", ".idea", ".vscode"
}

async def publish_progress(project_id: str, message: str, percent: int, eta_seconds: int = None):
    """Helper to send updates to the frontend via Redis Pub/Sub."""
    try:
        redis = Redis.from_url(REDIS_URL)
        event = {
            "type": "sync_progress",
            "project_id": project_id,
            "message": message,
            "percent": percent,
            "eta_seconds": eta_seconds
        }
        await redis.publish("game_events", json.dumps(event))
        await redis.close()
    except Exception as e:
        print(f"⚠️ Redis Publish Error: {e}")

async def ingest_project_repo(project_id: str, repo_url: str):
    """
    Clones a repo, walks the files, and indexes them into the Vector DB.
    Also runs Smart Project Sync to auto-generate Project Codex documentation.
    """
    await publish_progress(project_id, "Initializing workspace...", 5)
    
    # 1. Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        
        try:
            # Clone the repo (depth=1 for speed)
            await publish_progress(project_id, f"Cloning {repo_url}...", 10)
            git.Repo.clone_from(repo_url, temp_dir, depth=1)
            
            # --- 1. GENERATE PROJECT MAP ---
            await publish_progress(project_id, "Mapping structure...", 15)
            
            tree_lines = [f"Directory Structure for {repo_url}:"]
            files_to_index = []
            
            for root, dirs, files in os.walk(temp_dir):
                # Prune ignored directories in-place
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                
                # Calculate depth for indentation
                level = root.replace(temp_dir, '').count(os.sep)
                indent = ' ' * 4 * level
                folder_name = os.path.basename(root)
                
                if folder_name:
                    tree_lines.append(f"{indent}{folder_name}/")
                
                for file in files:
                    # Add to Tree View (all files for context)
                    tree_lines.append(f"{indent}    {file}")
                    
                    # Add to Index Queue if extension allows
                    ext = os.path.splitext(file)[1]
                    if ext in ALLOWED_EXTENSIONS or file in ["Dockerfile", "Makefile"]:
                        files_to_index.append(os.path.join(root, file))

            # Index the Map as a priority document
            map_content = "\n".join(tree_lines)
            await index_content(
                source_type="repo",
                source_id=f"{project_id}::PROJECT_MAP",
                content=f"File: PROJECT_MAP.md\nProject: {project_id}\n\n{map_content}"
            )
            # -------------------------------
            
            # 2. Scan files
            total_files = len(files_to_index)
            await publish_progress(project_id, f"Indexing {total_files} files...", 20)
            
            # --- SMART CODEX GENERATION START ---
            await publish_progress(project_id, "Analyzing for Project Codex...", 25)
            
            # Fetch project to get slug/name
            project_slug = "unknown"
            async for session in get_session():
                proj = await session.get(Project, project_id)
                if proj:
                    project_slug = proj.name.lower().replace(" ", "-")
            
            try:
                print(f"🔍 Starting Codex Analysis for {project_slug}...")
                # Initialize pipeline components
                scanner = RepoScanner()
                selector = CandidateSelector()
                generator = CodexDocGenerator()
                
                # Stage 1: Scan
                scan_results = scanner.scan(temp_dir)
                print(f"📊 Scan complete. Found {len(scan_results.get('core_docs', {}))} core docs.")
                
                # Doc types to generate
                doc_types = ["overview", "architecture", "data_model", "infra", "agents", "quest_hooks"]
                generated_count = 0
                
                async for session in get_session():
                    print("💾 DB Session acquired for Codex generation")
                    for doc_type in doc_types:
                        # Stage 2: Select Candidates
                        candidates = selector.select_candidates(temp_dir, doc_type, scan_results)
                        print(f"  - {doc_type}: Found {len(candidates)} candidates")
                        
                        if candidates:
                            # Stage 3: Generate
                            await publish_progress(project_id, f"Generating {doc_type}...", 25 + (generated_count * 5))
                            print(f"  - Generating {doc_type} doc...")
                            
                            doc_data = await generator.generate_doc(
                                project_slug=project_slug,
                                doc_type=doc_type,
                                file_snippets=candidates,
                                scan_meta=scan_results
                            )
                            
                            # Stage 4: Upsert
                            # Check existing
                            stmt = select(ProjectCodexDoc).where(
                                ProjectCodexDoc.project_id == project_id,
                                ProjectCodexDoc.doc_type == doc_type
                            )
                            existing = (await session.execute(stmt)).scalar_one_or_none()
                            
                            if existing:
                                # Update existing
                                existing.title = doc_data["title"]
                                existing.summary = doc_data["summary"]
                                existing.body_md = doc_data["body_md"]
                                existing.world_ids = doc_data["world_ids"]
                                existing.level = doc_data["level"]
                                existing.tags = doc_data["tags"]
                                existing.metadata_json = doc_data["metadata_json"]
                                existing.updated_at = datetime.utcnow()
                                session.add(existing)
                                print(f"  - Updated existing {doc_type} doc")
                            else:
                                # Create new
                                new_doc = ProjectCodexDoc(
                                    project_id=project_id,
                                    doc_type=doc_type,
                                    title=doc_data["title"],
                                    summary=doc_data["summary"],
                                    body_md=doc_data["body_md"],
                                    world_ids=doc_data["world_ids"],
                                    level=doc_data["level"],
                                    tags=doc_data["tags"],
                                    metadata_json=doc_data["metadata_json"]
                                )
                                session.add(new_doc)
                                print(f"  - Created new {doc_type} doc")
                            
                            generated_count += 1
                    
                    # Stage 5: Update Status
                    proj = await session.get(Project, project_id)
                    if proj:
                        # Determine status
                        has_overview = any(d == "overview" for d in doc_types) # Simplified check
                        # Real check would query DB, but we know what we just generated
                        
                        if generated_count >= 3:
                            proj.codex_status = "complete"
                        elif generated_count > 0:
                            proj.codex_status = "partial"
                        else:
                            proj.codex_status = "missing_docs"
                            
                        proj.codex_last_sync = datetime.utcnow()
                        session.add(proj)
                        print(f"📝 Updated Project status to {proj.codex_status}")
                    
                    await session.commit()
                    print("💾 DB Commit successful")
                    
            except Exception as e:
                print(f"⚠️ Smart Codex Generation Failed: {e}")
                import traceback
                traceback.print_exc()
                # Don't fail the whole sync, just log
            
            # --- SMART CODEX GENERATION END ---
            
            if total_files == 0:
                await publish_progress(project_id, "Done", 100, 0)
                return {"status": "ok", "files_indexed": 0}
            
            start_time = time.time()  # Start timer for ETA calculation
            
            # 3. Index Loop
            for idx, file_path in enumerate(files_to_index):
                # Calculate progress (50% to 90%) - shifted because of Codex gen
                progress = 50 + int((idx / total_files) * 40)
                
                # Throttle updates (every 10 files)
                if idx % 10 == 0 and idx > 0:
                    # Calculate Rate & ETA
                    elapsed = time.time() - start_time
                    rate = idx / elapsed  # files per second
                    remaining_files = total_files - idx
                    eta = int(remaining_files / rate) if rate > 0 else 0
                    
                    await publish_progress(project_id, f"Indexing files...", progress, eta)
                elif idx == 0:
                    await publish_progress(project_id, f"Indexing files...", progress)
                
                # Read content
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        
                    # Skip empty or massive files (>1MB)
                    if not content.strip() or len(content) > 1_000_000:
                        continue
                        
                    # Index into RAG
                    rel_path = os.path.relpath(file_path, temp_dir)
                    doc_id = f"{project_id}::{rel_path}"
                    
                    # Add context header
                    full_text = f"File: {rel_path}\nProject: {project_id}\n\n{content}"
                    
                    await index_content(
                        source_type="repo",
                        source_id=doc_id,
                        content=full_text
                    )
                    
                except Exception as e:
                    print(f"⚠️ Failed to read {file_path}: {e}")

            # 4. Done
            await publish_progress(project_id, "Done", 100, 0)
            
            # Send specific "Complete" event for the Toast
            redis = Redis.from_url(REDIS_URL)
            await redis.publish("game_events", json.dumps({
                "type": "sync_complete",
                "title": "SYNC COMPLETE",
                "message": f"Updated knowledge base & Codex for {repo_url}.",
                "project_id": project_id
            }))
            await redis.close()

            print(f"✅ Successfully indexed {total_files} files for {project_id}")
            return {"status": "ok", "files_indexed": total_files}

        except Exception as e:
            await publish_progress(project_id, f"Error: {str(e)}", 0)
            print(f"❌ Ingestion Failed: {e}")
            return {"status": "error", "message": str(e)}
