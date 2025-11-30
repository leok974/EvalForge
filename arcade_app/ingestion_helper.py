import os
import shutil
import tempfile
import git
import json
import time
from typing import List, Dict
from redis.asyncio import Redis
from arcade_app.rag_helper import index_content

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
    Broadcasting progress events via Redis.
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
            
            if total_files == 0:
                await publish_progress(project_id, "Done", 100, 0)
                return {"status": "ok", "files_indexed": 0}
            
            start_time = time.time()  # Start timer for ETA calculation
            
            # 3. Index Loop
            for idx, file_path in enumerate(files_to_index):
                # Calculate progress (20% to 90%)
                progress = 20 + int((idx / total_files) * 70)
                
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
                "message": f"Updated knowledge base for {repo_url}.",
                "project_id": project_id
            }))
            await redis.close()

            print(f"✅ Successfully indexed {total_files} files for {project_id}")
            return {"status": "ok", "files_indexed": total_files}

        except Exception as e:
            await publish_progress(project_id, f"Error: {str(e)}", 0)
            print(f"❌ Ingestion Failed: {e}")
            return {"status": "error", "message": str(e)}
