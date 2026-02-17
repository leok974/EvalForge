from __future__ import annotations
import os
import time
import tempfile
import subprocess
import glob
import logging
from dataclasses import dataclass
from arcade_app.services.runner_registry import RunnerRegistry

# Startup Log
print(f"DEBUG: code_runner_docker initialized. Version: Hardening-v1")
logger = logging.getLogger("code_runner")

@dataclass
class ExecResult:
    ok: bool
    exit_code: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool

from typing import Optional, Dict, Any

def run_code_docker(language: str, code: str, stdin: str = "", timeout_ms: int = 2500, workspace: Optional[Dict[str, Any]] = None, mode: str = "run", quest_slug: Optional[str] = None) -> ExecResult:
    """
    Safer execution: docker container, no network, capped resources, non-root, read-only.
    Requires docker installed + daemon running.
    """
    # 1. Determine Entrypoint
    entrypoint = "main.py"
    if language == "typescript": entrypoint = "main.ts"
    
    if workspace:
        entrypoint = workspace.get("entrypoint", entrypoint)
    elif code:
        pass # Legacy single file, defaults apply
    
    spec = RunnerRegistry.get_runner(language, mode=mode, entrypoint=entrypoint)
    image = os.getenv(f"EXECUTION_DOCKER_IMAGE_{language.upper()}", spec.docker_image)
    
    t0 = time.time()

    with tempfile.TemporaryDirectory(prefix="evalforge-docker-run-") as td:
        
        # 2. Write Files
        files = workspace.get("files", []) if workspace else []
        
        # Fallback: If no files provided, try to load from disk using quest_slug
        if not files and quest_slug:
            quest_dir = os.path.join("d:\\EvalForge\\data\\quests", quest_slug, "workspace")
            if os.path.exists(quest_dir):
                logger.info(f"Fallback: Loading workspace from {quest_dir}")
                for root, _, filenames in os.walk(quest_dir):
                    for filename in filenames:
                        abs_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(abs_path, quest_dir)
                        # Skip hidden files/dirs
                        if any(p.startswith(".") for p in rel_path.split(os.sep)):
                            continue
                        try:
                            with open(abs_path, "r", encoding="utf-8") as f:
                                files.append({"path": rel_path, "content": f.read()})
                        except Exception:
                            pass # Skip binary or unreadable
            else:
                 # Check if it is a specific quest-lines structure (e.g. data/quests/javascript/...)
                 # This is harder without the map. But audit script fixed paths.
                 pass

        # If still no files and we have 'code', use legacy mode
        if not files and code:
             # Legacy Single File
            main_file = os.path.join(td, spec.file_name)
            with open(main_file, "w", encoding="utf-8") as f:
                f.write(code)
        else:
            for f in files:
                path = f["path"]
                content = f["content"]
                # Prevent traversal
                if ".." in path or path.startswith("/"): continue
                
                # Path Normalization: Option B (Strip workspace/ prefix)
                # We want files to land in 'td' such that when 'td' is CP'd to '/workspace',
                # the file is at '/workspace/<entrypoint>'.
                # Any 'workspace/' prefix in the artifact path is redundant if the container IS the workspace.
                if path.startswith("workspace/") or path.startswith("workspace\\"):
                    path = path[10:]  # len("workspace/")
                elif path.startswith("workspace") and (len(path) > 9 and path[9] in [os.sep, '/']):
                     path = path[10:]

                full_path = os.path.join(td, path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as wf:
                    wf.write(content)

            # Inject Python Test Runner
            if mode == "tests" and language == "python":
                runner_dir = os.path.join(td, ".evalforge")
                os.makedirs(runner_dir, exist_ok=True)
                runner_target = os.path.join(runner_dir, "run_unittest_json.py")
                
                # Source path assumption: same specific directory
                src_path = os.path.join(os.path.dirname(__file__), "run_unittest_json.py")
                if os.path.exists(src_path):
                    with open(src_path, "r", encoding="utf-8") as rf:
                        with open(runner_target, "w", encoding="utf-8") as wf:
                            wf.write(rf.read())
            
            # 3. Permissions fix for Docker (since we run as non-root user)
            # Ensure the temp dir and all files are world-readable AND writable
            os.chmod(td, 0o777)
            for root, dirs, files_in_dir in os.walk(td):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o777)
                for f in files_in_dir:
                    os.chmod(os.path.join(root, f), 0o666)

        # 4. PREFLIGHT CHECK & ENTRYPOINT RESOLUTION
        # List files to verify
        listing = []
        for root, _, filenames in os.walk(td):
            for f in filenames:
                listing.append(os.path.relpath(os.path.join(root, f), td))
        
        # Determine Entrypoint dynamically if not strictly enforced by workspace config
        # The user says: "Prefer configured entrypoint only if present, else task.py, else main.py"
        
        # spec.file_name came from Registry (defaults to main.py/main.ts). 
        # But if the workspace has 'task.py' and we are python, we should switch.
        
        effective_entrypoint = spec.file_name # Default (e.g. main.py)
        
        # If workspace explicitly requested an entrypoint, check if it exists
        found_configured = False
        if workspace and workspace.get("entrypoint"):
             if workspace["entrypoint"] in listing:
                 effective_entrypoint = workspace["entrypoint"]
                 found_configured = True
        
        # Else, if we haven't found a configured one, AND we are in Python (or generally), 
        # try to detect 'task.py' vs 'main.py'
        if not found_configured and language == "python":
            if "task.py" in listing:
                effective_entrypoint = "task.py"
            elif "main.py" in listing:
                effective_entrypoint = "main.py"
        
        # For other languages, we might want similar logic (e.g. task.js vs index.js), 
        # but User specifically asked for this for Python.
        
        # Check if resolved entrypoint exists
        if effective_entrypoint not in listing:
             # Preflight Failed
             error_msg = f"SYSTEM_ERROR: WORKSPACE_MISSING: Entrypoint '{effective_entrypoint}' not found in workspace.\n"
             error_msg += f"Written files: {listing}\n"
             # error_msg += f"Files supplied: {[f.get('path') for f in files]}\n" 
             return ExecResult(
                ok=False,
                exit_code=2, # ENOENT-like
                duration_ms=0,
                stdout="",
                stderr=error_msg,
                timed_out=False
             )

        # Update spec command to use the effective entrypoint
        # The spec.command is likely ["python", "main.py"] or similar.
        # We need to swap the filename.
        # This is a bit hacky but safer than parsing the command list.
        # Python runner command is typically ["python", "-B", "main.py"] (or similar in registry)
        # We will reconstruct it.
        
        final_command = list(spec.command)
        # If the last argument looks like a filename, replace it? 
        # Or just specific knowledge of python runner?
        if language == "python":
             # Registry for python: ["python", "-I", "-B", "main.py"] or similar.
             # We just need to ensure we run python <entrypoint>
             # Let's rebuild it to be safe.
             final_command = ["python", "-I", "-B", effective_entrypoint]
        elif language == "javascript" or language == "typescript":
             # node main.js / ts-node main.ts
             # If we detected a different file, swap the last arg
             if final_command and final_command[-1] == spec.file_name:
                 final_command[-1] = effective_entrypoint

        # 5. Docker-in-Docker safe execution
        import uuid
        container_name = f"runner-{uuid.uuid4()}"
        
        # Base Create Command
        create_cmd = [
            "docker", "create",
            "--name", container_name,
            "--network", "none",
            "--cpus", "1",
            "--memory", "256m",
            "--pids-limit", "64",
            "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", "65534:65534",
            "-w", "/workspace",
            # Env vars
            *sum([["-e", f"{k}={v}"] for k, v in spec.env.items()], []),
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "-e", "PYTHONIOENCODING=utf-8",
            image,
            *final_command # Use the updated command
        ]

        try:
            # A) Create
            subprocess.check_call(create_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # B) Copy files
            cp_cmd = ["docker", "cp", f"{td}/.", f"{container_name}:/workspace/"]
            subprocess.check_call(cp_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # C) Start (Detached)
            subprocess.check_call(["docker", "start", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # D) Wait
            wait_cmd = ["docker", "wait", container_name]
            try:
                subprocess.run(wait_cmd, timeout=max(0.1, (timeout_ms + 1000) / 1000.0), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.TimeoutExpired:
                 pass
            
            # E) Logs
            logs_p = subprocess.run(
                ["docker", "logs", container_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout_str = logs_p.stdout.decode("utf-8", errors="replace")
            stderr_str = logs_p.stderr.decode("utf-8", errors="replace")
            
            # Fallback for reports
            if not stdout_str.strip() or (mode == "tests" and not stdout_str.strip().startswith("{")):
                try:
                    report_dest = os.path.join(td, "test_results_fallback.json")
                    subprocess.check_call(
                        ["docker", "cp", f"{container_name}:/workspace/.evalforge/test_results.json", report_dest],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    with open(report_dest, "r", encoding="utf-8") as f:
                        fallback_json = f.read()
                        if fallback_json:
                             stdout_str = fallback_json
                except Exception:
                    pass

            # F) Inspect Exit Code
            inspect_p = subprocess.run(
                ["docker", "inspect", container_name, "--format", "{{.State.ExitCode}}"],
                stdout=subprocess.PIPE
            )
            exit_code = int(inspect_p.stdout.decode().strip() or "0")
            
            dt = int((time.time() - t0) * 1000)
            
            return ExecResult(
                ok=(exit_code == 0),
                exit_code=exit_code,
                duration_ms=dt,
                stdout=stdout_str,
                stderr=stderr_str,
                timed_out=False,
            )

        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "kill", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logs_p = subprocess.run(["docker", "logs", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = logs_p.stdout.decode("utf-8", errors="replace")
            err = logs_p.stderr.decode("utf-8", errors="replace")
            dt = int((time.time() - t0) * 1000)
            return ExecResult(
                ok=False,
                exit_code=None,
                duration_ms=dt,
                stdout=out,
                stderr=err + "\n[Timed out]",
                timed_out=True,
            )
        except Exception as e:
             return ExecResult(
                ok=False,
                exit_code=-1,
                duration_ms=0,
                stdout="",
                stderr=str(e),
                timed_out=False
             )
        finally:
            subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
