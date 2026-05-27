from __future__ import annotations
import os
import time
import tempfile
import subprocess
import glob
import logging
import json
from dataclasses import dataclass
from arcade_app.services.runner_registry import RunnerRegistry
from arcade_app.services.logging_helper import debug_log

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
    artifacts: Optional[Dict[str, Any]] = None
    selenium_trace: Optional[list] = None

from arcade_app.services.code_runner import _parse_selenium_trace, _strip_selenium_trace_sentinel

from typing import Optional, Dict, Any

def run_code_docker(language: str, code: str, stdin: str = "", timeout_ms: int = 2500, workspace: Optional[Dict[str, Any]] = None, mode: str = "run", entrypoint: Optional[str] = None, quest_slug: Optional[str] = None) -> ExecResult:
    """
    Safer execution: docker container, no network, capped resources, non-root, read-only.
    Requires docker installed + daemon running.
    """
    container_name = f"evalforge-run-{int(time.time()*1000)}"
    t0 = time.time()

    # 1. Determine Internal Entrypoint (for registry lookups)
    # NOTE: Must explicitly prioritize the `entrypoint` parameter — a bare ternary like
    # `entrypoint or "task.sql" if language == "sql" else ...` has wrong precedence in Python.
    if entrypoint:
        resolved_entrypoint = entrypoint
    elif language == "sql":
        resolved_entrypoint = "task.sql"
    elif language == "typescript":
        # Only trust a workspace entrypoint that is actually a .ts file.
        # build_effective_workspace defaults entrypoint to "main.py" for all languages,
        # so we must ignore that default for TypeScript.
        ws_ep = workspace.get("entrypoint") if workspace else None
        if ws_ep and ws_ep.endswith(".ts"):
            resolved_entrypoint = ws_ep
        else:
            resolved_entrypoint = "main.ts"
    elif workspace:
        resolved_entrypoint = workspace.get("entrypoint") or "main.py"
    else:
        resolved_entrypoint = "main.py"
    
    spec = RunnerRegistry.get_runner(language, mode=mode, entrypoint=resolved_entrypoint)
    image = os.getenv(f"EXECUTION_DOCKER_IMAGE_{language.upper()}", spec.docker_image)

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

        # 3. Handle other files from workspace/fallback
        if files:
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

        # 4. Always write 'code' to the entrypoint if provided (overriding or as main)
        # We do this LAST so it overrides any file from the workspace with the same name
        if code:
            # We use resolved_entrypoint which was determined at the start
            main_file = os.path.join(td, resolved_entrypoint or "task.sql")
            os.makedirs(os.path.dirname(main_file), exist_ok=True)
            with open(main_file, "w", encoding="utf-8") as f:
                f.write(code)

        # Inject Python Test Runner — must happen regardless of whether `code` is
        # non-empty, otherwise the runner container starts without the script and
        # Python raises "can't open file '/workspace/.evalforge/run_unittest_json.py'".
        if mode == "tests" and (language == "python" or language == "sql"):
            runner_dir = os.path.join(td, ".evalforge")
            os.makedirs(runner_dir, exist_ok=True)
            runner_target = os.path.join(runner_dir, "run_unittest_json.py")
            src_path = os.path.join(os.path.dirname(__file__), "run_unittest_json.py")
            if os.path.exists(src_path):
                with open(src_path, "r", encoding="utf-8") as rf:
                    with open(runner_target, "w", encoding="utf-8") as wf:
                        wf.write(rf.read())
        # Determine Runner Script
        db_engine = workspace.get("db_engine", "sqlite") if workspace else "sqlite"
        
        # Fallback for db_engine if quest_slug is provided
        if not workspace and quest_slug:
             # Look for quest.json to find db_engine
             quest_json_path = os.path.join("d:\\EvalForge\\data\\quests", quest_slug, "quest.json")
             if os.path.exists(quest_json_path):
                 try:
                     with open(quest_json_path, "r", encoding="utf-8") as f:
                         qdata = json.load(f)
                         db_engine = qdata.get("db_engine", "sqlite")
                         logger.info(f"Fallback: Loaded db_engine '{db_engine}' from {quest_json_path}")
                 except Exception as e:
                     logger.error(f"Fallback Error: Failed to load quest.json for engine: {e}")

        is_postgres = db_engine == "postgres"
        listing = [f["path"] for f in files]
        found_configured = bool(workspace.get("entrypoint")) if workspace else False
        
        effective_entrypoint = entrypoint or resolved_entrypoint

        if not effective_entrypoint:
            if language == "sql":
                effective_entrypoint = "task.sql"
            elif language == "typescript":
                effective_entrypoint = "main.ts"
            elif language == "javascript":
                effective_entrypoint = "main.js"
            elif language == "python":
                # Use workspace-configured entrypoint if set; otherwise auto-detect from files
                ws_entrypoint = workspace.get("entrypoint") if workspace else None
                if ws_entrypoint:
                    effective_entrypoint = ws_entrypoint
                elif "task.py" in listing:
                    effective_entrypoint = "task.py"
                elif "main.py" in listing:
                    effective_entrypoint = "main.py"
        
        final_command = None

        # Inject runners
        if mode == "run" and language == "sql":
            runner_dir = os.path.join(td, ".evalforge")
            os.makedirs(runner_dir, exist_ok=True)
            
            if is_postgres:
                runner_file = "postgres_runner.py"
                src_path = os.path.join(os.path.dirname(__file__), "runners", "postgres_runner.py")
                final_command = ["python", "-u", "-I", "-B", "/workspace/.evalforge/postgres_runner.py"]
            else:
                runner_file = "sql_preview.py"
                src_path = os.path.join(os.path.dirname(__file__), "runners", "sql_preview.py")
                final_command = ["python", "-u", "-I", "-B", "/workspace/.evalforge/sql_preview.py"]

            runner_target = os.path.join(runner_dir, runner_file)
            if os.path.exists(src_path):
                with open(src_path, "r", encoding="utf-8") as rf:
                    with open(runner_target, "w", encoding="utf-8") as wf:
                        wf.write(rf.read())
            
            # Phase 9.8: Ensure artifacts dir is writable by container user
            try:
                if os.name == 'nt':
                     # On Windows bit manipulation is tricky, but we can try
                     pass 
                else:
                     subprocess.run(["chmod", "-R", "777", runner_dir], check=True)
            except Exception: pass
            
        if language == "python":
            runner_dir = os.path.join(td, ".evalforge")
            os.makedirs(runner_dir, exist_ok=True)
            sel_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "runtimes", "python", "selenium"))
            if os.path.exists(sel_src):
                for file_name in ["step_logger.py", "helpers.py"]:
                    sf = os.path.join(sel_src, file_name)
                    df = os.path.join(runner_dir, file_name)
                    if os.path.exists(sf):
                        with open(sf, "r", encoding="utf-8") as rf:
                            with open(df, "w", encoding="utf-8") as wf:
                                wf.write(rf.read())
            try:
                if os.name != 'nt':
                    subprocess.run(["chmod", "-R", "777", runner_dir], check=True)
            except Exception: pass
        
        # Check if resolved entrypoint exists
        
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
        
        if not final_command:
            final_command = list(spec.command)
        # If the last argument looks like a filename, replace it?
        # Or just specific knowledge of python runner?
        if language == "python" and mode != "tests":
             # Registry for python: ["python", "-I", "-B", "main.py"] or similar.
             # We just need to ensure we run python <entrypoint>
             # Let's rebuild it to be safe.
             # NOTE: Do NOT override for mode="tests" — the registry command runs run_unittest_json.py
             final_command = ["python", "-I", "-B", effective_entrypoint]
        elif language == "javascript" or language == "typescript":
             # node main.js / ts-node main.ts
             # If we detected a different file, swap the last arg
             if final_command and final_command[-1] == spec.file_name:
                 final_command[-1] = effective_entrypoint

        debug_log(f"DEBUG[code_runner_docker]: final_command={final_command}")

        # Phase 9.3: Docker networking and env vars for Postgres
        network_name = os.getenv("EVALFORGE_RUNNER_NETWORK", "evalforge_evalforge")
        artifacts_dir = "/workspace/.evalforge"
        
        # High-entropy surrogate ID (ms + random)
        import random
        surrogate_id = f"{int(time.time()*1000)}_{random.randint(1000, 9999)}"
        
        create_cmd = [
            "docker", "create",
            "--name", container_name,
            "--network", network_name if is_postgres else "none",
            "--cpus", "1",
            "--memory", "256m",
            "-e", "GIT_EDITOR=true",
            "-e", "GIT_TERMINAL_PROMPT=0",
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
            "-e", "PYTHONPATH=/workspace:/workspace/.evalforge",
            "-e", f"EVALFORGE_ARTIFACTS_DIR={artifacts_dir}",
            # Pass PG Config if needed
            "-e", f"PG_DB_URL=postgresql://evalforge:evalforge@db:5432/evalforge",
            "-e", f"PG_TEMP_SCHEMA=run_{surrogate_id[:8]}",
            "-e", f"EVALFORGE_SQL_ENTRYPOINT={effective_entrypoint}",
            "-e", f"EVALFORGE_APP_URL={os.getenv('EVALFORGE_APP_URL', 'http://host.docker.internal:8765')}",
            image,
            *final_command # Use the updated command
        ]

        try:
            # A) Create
            debug_log(f"Phase 9.4: Creating container {container_name} with image {image}")
            subprocess.check_call(create_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # B) Copy files
            debug_log(f"Phase 9.5: Copying workspace files from {td}")
            cp_cmd = ["docker", "cp", f"{td}/.", f"{container_name}:/workspace/"]
            subprocess.check_call(cp_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # C) Start (Detached)
            debug_log(f"Phase 9.6: Starting container {container_name}")
            subprocess.check_call(["docker", "start", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # D) Wait
            debug_log(f"Phase 9.7: Waiting for container completion (timeout {timeout_ms}ms)")
            wait_cmd = ["docker", "wait", container_name]
            try:
                subprocess.run(wait_cmd, timeout=max(0.1, (timeout_ms + 1000) / 1000.0), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.TimeoutExpired:
                 debug_log(f"Phase 9.8: Container {container_name} timed out")
                 pass
            
            # E) Logs
            logs_p = subprocess.run(
                ["docker", "logs", container_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout_str = logs_p.stdout.decode("utf-8", errors="replace")
            stderr_str = logs_p.stderr.decode("utf-8", errors="replace")
            
            import logging
            logging.error(f"DOCKER STDOUT: {stdout_str}")
            logging.error(f"DOCKER STDERR: {stderr_str}")

            # Fallback for reports
            if not stdout_str.strip() or (mode == "tests" and not stdout_str.strip().startswith("{")):
                try:
                    report_dest = os.path.join(td, "test_results_fallback.json")
                    subprocess.check_call(
                        ["docker", "cp", f"{container_name}:{artifacts_dir}/test_results.json", report_dest],
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
            
            # G) Capture artifacts
            artifacts_out = {}
            
            # Recursive copy of .evalforge directory to capture everything (SQL + Selenium + Screenshots)
            try:
                subprocess.run(
                    ["docker", "cp", f"{container_name}:{artifacts_dir}/.", td],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    timeout=5
                )
            except Exception:
                pass

            # 1. First try to extract from stdout marker (fast path for small JSON)
            import re
            match = re.search(r'<<EVALFORGE_ARTIFACTS_START>>(.*?)<<EVALFORGE_ARTIFACTS_END>>', stdout_str, re.DOTALL)
            if match:
                try:
                    memory_artifacts = json.loads(match.group(1))
                    for k, v in memory_artifacts.items():
                        artifacts_out[k] = v
                except Exception:
                    pass
                # Strip it from stdout so it doesn't clutter UI logs
                stdout_str = re.sub(r'\n?<<EVALFORGE_ARTIFACTS_START>>.*?<<EVALFORGE_ARTIFACTS_END>>\n?', '', stdout_str, flags=re.DOTALL)
                
            # Parse and strip Phase 18 Selenium trace
            selenium_trace = _parse_selenium_trace(stdout_str)
            stdout_str = _strip_selenium_trace_sentinel(stdout_str)
                
            # 2. Load artifacts from the copied directory
            # SQL
            for aname in ["sql_trace", "sql_student_result", "sql_explain"]:
                if not artifacts_out.get(aname):
                    p = os.path.join(td, f"{aname}.json")
                    if os.path.exists(p):
                        try:
                            with open(p, "r", encoding="utf-8") as f:
                                artifacts_out[aname] = json.load(f)
                        except Exception: pass
            
            # Selenium
            p_sel = os.path.join(td, "selenium_artifacts.json")
            if os.path.exists(p_sel):
                try:
                    with open(p_sel, "r", encoding="utf-8") as f:
                        artifacts_out["selenium"] = json.load(f)
                        # We also want to keep the local 'td' path for persistence later
                        artifacts_out["_local_dir"] = td 
                except Exception: pass

            dt = int((time.time() - t0) * 1000)
            
            return ExecResult(
                ok=(exit_code == 0),
                exit_code=exit_code,
                duration_ms=dt,
                stdout=stdout_str,
                stderr=stderr_str,
                timed_out=False,
                artifacts=artifacts_out if artifacts_out else None,
                selenium_trace=selenium_trace
            )

        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "kill", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logs_p = subprocess.run(["docker", "logs", container_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = logs_p.stdout.decode("utf-8", errors="replace")
            err = logs_p.stderr.decode("utf-8", errors="replace")
            dt = int((time.time() - t0) * 1000)

            artifacts_out = {}
            import re
            
            # 1. First try to extract from stdout marker
            match = re.search(r'<<EVALFORGE_ARTIFACTS_START>>(.*?)<<EVALFORGE_ARTIFACTS_END>>', out, re.DOTALL)
            if match:
                try:
                    memory_artifacts = json.loads(match.group(1))
                    for k, v in memory_artifacts.items():
                        artifacts_out[k] = v
                except Exception:
                    pass
                # Strip it from stdout so it doesn't clutter UI logs
                out = re.sub(r'\n?<<EVALFORGE_ARTIFACTS_START>>.*?<<EVALFORGE_ARTIFACTS_END>>\n?', '', out, flags=re.DOTALL)
                
            # Parse and strip Phase 18 Selenium trace for timeout path
            selenium_trace = _parse_selenium_trace(out)
            out = _strip_selenium_trace_sentinel(out)
                
            # 2. Fallback to disk if not fully populated
            for aname in ["sql_trace", "sql_student_result", "sql_explain"]:
                if not artifacts_out.get(aname):
                    try:
                        dest = os.path.join(td, f"{aname}.json")
                        subprocess.run(
                            ["docker", "cp", f"{container_name}:{artifacts_dir}/{aname}.json", dest],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            timeout=3
                        )
                        if os.path.exists(dest):
                            with open(dest, "r", encoding="utf-8") as f:
                                artifacts_out[aname] = json.load(f)
                    except Exception:
                        pass

            return ExecResult(
                ok=False,
                exit_code=None,
                duration_ms=dt,
                stdout=out,
                stderr=err + "\n[Timed out]",
                timed_out=True,
                artifacts=artifacts_out if artifacts_out else None,
                selenium_trace=selenium_trace
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
            # G) Cleanup (TEMPORARILY DISABLED FOR DEBUG)
            # subprocess.run(["docker", "rm", "-f", container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            pass
