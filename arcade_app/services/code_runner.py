from __future__ import annotations
import os
import sys
import time
import tempfile
import subprocess
from arcade_app.services.logging_helper import debug_log
from dataclasses import dataclass


@dataclass
class ExecResult:
    ok: bool
    exit_code: int | None
    duration_ms: int
    stdout: str
    stderr: str
    timed_out: bool
    state: Optional[Dict[str, Any]] = None  # Captured state (files, git, etc.)
    artifacts: Optional[Dict[str, Any]] = None # Captured JSON artifacts from harness
    selenium_trace: Optional[list] = None  # Phase 18: Step trace

def run_python_local(code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None, quest_slug: Optional[str] = None, entrypoint: Optional[str] = None) -> ExecResult:
    """
    DEV ONLY. Not safe for untrusted code. Use docker backend for prod.
    Runs python with:
      -I isolated mode, -B no bytecode
    """
    t0 = time.time()
    import logging
    logger = logging.getLogger("code_runner")

    with tempfile.TemporaryDirectory(prefix="evalforge-run-") as td:
        # Write workspace files if present
        files = workspace.get("files", []) if workspace else []

        # Fallback: If no files provided, try to load from disk using quest_slug
        if not files and quest_slug:
            # Need to find where data/quests is relative to CWD
            # app is usually at d:\EvalForge or /app in container
            # Try a few standard locations
            possible_roots = ["/app/data/quests", "d:\\EvalForge\\data\\quests", "./data/quests", "../data/quests"]
            quest_dir = None
            for r in possible_roots:
                p = os.path.join(r, quest_slug, "workspace")
                if os.path.exists(p):
                    quest_dir = p
                    break
            
            if quest_dir:
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
                            pass 

        has_main = False
        
        if not files and code:
             # Legacy Single File
             path = os.path.join(td, "main.py")
             with open(path, "w", encoding="utf-8") as f:
                 f.write(code)
             has_main = True
        elif files:
             for f in files:
                 path = f["path"]
                 content = f["content"]
                 # Prevent traversal
                 if ".." in path or path.startswith("/"): continue
                 
                 # Path Normalization: Strip workspace/ prefix
                 if path.startswith("workspace/") or path.startswith("workspace\\"):
                     path = path[10:]
                 elif path.startswith("workspace") and (len(path) > 9 and path[9] in [os.sep, '/']):
                     path = path[10:]
                     
                 if os.path.normpath(path) == "main.py":
                     has_main = True

                 full_path = os.path.join(td, path)
                 os.makedirs(os.path.dirname(full_path), exist_ok=True)
                 with open(full_path, "w", encoding="utf-8") as fw:
                     fw.write(content)
        
        # Injected code override (critical for running solutions with workspace)
        if code and files:
             path = os.path.join(td, "main.py")
             with open(path, "w", encoding="utf-8") as f:
                 f.write(code)
             has_main = True
                         
        # Determine target file
        target_file = "main.py"
        if workspace and workspace.get("entrypoint"):
            target_file = workspace["entrypoint"]
            # Normalize entrypoint too if it has workspace/
            if target_file.startswith("workspace/") or target_file.startswith("workspace\\"):
                target_file = target_file[10:]

        # Preflight Check & Entrypoint Resolution
        listing = []
        for root, _, filenames in os.walk(td):
            for f in filenames:
                listing.append(os.path.relpath(os.path.join(root, f), td))

        effective_entrypoint = entrypoint or "main.py"
        found_entry = False
        
        # Priority 1: Use explicitly provided entrypoint (if it exists in workspace)
        if entrypoint and entrypoint in listing:
            effective_entrypoint = entrypoint
            found_entry = True
            
        # Priority 2: Fallback to workspace metadata entrypoint
        if not found_entry and workspace and workspace.get("entrypoint"):
             normalized_ws_entry = workspace["entrypoint"]
             if normalized_ws_entry.startswith("workspace/") or normalized_ws_entry.startswith("workspace\\"):
                 normalized_ws_entry = normalized_ws_entry[10:]
             
             if normalized_ws_entry in listing:
                 effective_entrypoint = normalized_ws_entry
                 found_entry = True
                 
        # Priority 3: Auto-detection
        if not found_entry:
            if "task.py" in listing:
                effective_entrypoint = "task.py"
            elif "main.py" in listing:
                effective_entrypoint = "main.py"
        
        path = os.path.join(td, effective_entrypoint)
        if not os.path.exists(path):
            error_msg = f"SYSTEM_ERROR: WORKSPACE_MISSING: Entrypoint '{effective_entrypoint}' not found in workspace.\n"
            error_msg += f"Written files: {listing}\n"
            return ExecResult(
                ok=False,
                exit_code=2, 
                duration_ms=0,
                stdout="",
                stderr=error_msg,
                timed_out=False
             )
        
        # Using sys.executable is safer for local dev if venv is active.
        cmd = [sys.executable, "-B", path]

        # Inherit system environment (critical for Windows DLLs/PATH)
        env = os.environ.copy()
        sel_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "runtimes", "python", "selenium"))
        env.update({
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": f"{td}{os.pathsep}{sel_path}",
            "GIT_EDITOR": "true",
            "GIT_TERMINAL_PROMPT": "0",
            # EVALFORGE_APP_URL is set to http://mock-cms:8765 by docker-compose.yml (compose dev stack).
            # Falls back to host.docker.internal for non-compose local dev only.
            "EVALFORGE_APP_URL": os.getenv("EVALFORGE_APP_URL", "http://host.docker.internal:8765"),
        })

        try:
            p = subprocess.run(
                cmd,
                input=stdin.encode("utf-8") if stdin else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=td,
                env=env,
                timeout=max(0.1, timeout_ms / 1000.0),
            )
            
            dt = int((time.time() - t0) * 1000)
            
            # Capture state before cleanup
            state = _capture_state(td)
            artifacts = _capture_artifacts(td)
            raw_stdout = p.stdout.decode("utf-8", errors="replace")
            selenium_trace = _parse_selenium_trace(raw_stdout)
            
            return ExecResult(
                ok=(p.returncode == 0),
                exit_code=p.returncode,
                duration_ms=dt,
                stdout=_strip_selenium_trace_sentinel(raw_stdout),
                stderr=p.stderr.decode("utf-8", errors="replace"),
                timed_out=False,
                state=state,
                artifacts=artifacts,
                selenium_trace=selenium_trace
            )
        except subprocess.TimeoutExpired as e:
            dt = int((time.time() - t0) * 1000)
            out = (e.stdout or b"").decode("utf-8", errors="replace")
            err = (e.stderr or b"").decode("utf-8", errors="replace")
            selenium_trace = _parse_selenium_trace(out)
            return ExecResult(
                ok=False,
                exit_code=None,
                duration_ms=dt,
                stdout=_strip_selenium_trace_sentinel(out),
                stderr=err + ("\n[Timed out]" if err else "[Timed out]"),
                timed_out=True,
                state=_capture_state(td),
                artifacts=_capture_artifacts(td),
                selenium_trace=selenium_trace
            )

import hashlib
from pathlib import Path

import json

def _capture_artifacts(temp_dir_str: str) -> Dict[str, Any]:
    temp_dir = Path(temp_dir_str)
    artifacts = {}
    for aname in ["sql_trace", "sql_student_result", "sql_explain"]:
        path = temp_dir / f"{aname}.json"
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    artifacts[aname] = json.load(f)
            except Exception:
                pass
    return artifacts if artifacts else None


_TRACE_START = "<<EVALFORGE_SELENIUM_TRACE_START>>"
_TRACE_END = "<<EVALFORGE_SELENIUM_TRACE_END>>"


def _parse_selenium_trace(stdout: str) -> list | None:
    """Extract and parse the selenium step trace sentinel from stdout."""
    try:
        s = stdout.find(_TRACE_START)
        e = stdout.find(_TRACE_END)
        if s == -1 or e == -1:
            return None
        payload = stdout[s + len(_TRACE_START):e]
        data = json.loads(payload)
        return data.get("steps")
    except Exception:
        return None


def _strip_selenium_trace_sentinel(stdout: str) -> str:
    """Remove the selenium trace sentinel from the stdout string."""
    try:
        s = stdout.find(_TRACE_START)
        e = stdout.find(_TRACE_END)
        if s == -1 or e == -1:
            return stdout
        return stdout[:s].rstrip() + stdout[e + len(_TRACE_END):]
    except Exception:
        return stdout

def _capture_state(temp_dir_str: str) -> Dict[str, Any]:
    """Capture state: files, hashes, git info."""
    temp_dir = Path(temp_dir_str)
    state = {
        "files": [],
        "hashes": {},
        "git": {}
    }
    
    # 1. Files & Hashes
    all_files = []
    try:
        for p in temp_dir.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                try:
                    rel_path = p.relative_to(temp_dir).as_posix()
                    all_files.append(rel_path)
                    
                    # Calculate hash
                    sha256 = hashlib.sha256()
                    with open(p, "rb") as f:
                        while chunk := f.read(8192):
                            sha256.update(chunk)
                    state["hashes"][rel_path] = sha256.hexdigest()
                except Exception:
                    pass
    except Exception:
        pass
            
    state["files"] = sorted(all_files)
    
    # 2. Git State
    if (temp_dir / ".git").exists():
        try:
             # git status
             p = subprocess.run(["git", "status", "--porcelain"], cwd=temp_dir, capture_output=True, text=True)
             state["git"]["status_porcelain"] = p.stdout.strip()
             
             # git log
             p = subprocess.run(["git", "log", "-n", "10", "--oneline"], cwd=temp_dir, capture_output=True, text=True)
             logs = p.stdout.strip().split('\n') if p.stdout.strip() else []
             state["git"]["log_oneline"] = [l.strip() for l in logs if l.strip()]
             
             # git branch
             p = subprocess.run(["git", "branch", "--show-current"], cwd=temp_dir, capture_output=True, text=True)
             state["git"]["branch"] = p.stdout.strip()
             
             state["git"]["has_dot_git"] = True
        except Exception as e:
            state["git"]["error"] = str(e)
    else:
        state["git"]["has_dot_git"] = False
        
    return state

from typing import Optional, Dict, Any

def run_javascript_local(code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None, quest_slug: Optional[str] = None, entrypoint: Optional[str] = None) -> ExecResult:
    """
    DEV ONLY. Runs javascript locally using 'node'.
    """
    t0 = time.time()
    import logging
    logger = logging.getLogger("code_runner")

    with tempfile.TemporaryDirectory(prefix="evalforge-run-js-") as td:
        # Write workspace files
        files = workspace.get("files", []) if workspace else []

        if not files and quest_slug:
             # Load from disk fallback
             possible_roots = ["/app/data/quests", "d:\\EvalForge\\data\\quests", "./data/quests", "../data/quests"]
             quest_dir = None
             for r in possible_roots:
                 p = os.path.join(r, quest_slug, "workspace")
                 if os.path.exists(p):
                     quest_dir = p
                     break
             
             if quest_dir:
                 logger.info(f"Fallback: Loading workspace from {quest_dir}")
                 for root, _, filenames in os.walk(quest_dir):
                     for filename in filenames:
                         abs_path = os.path.join(root, filename)
                         rel_path = os.path.relpath(abs_path, quest_dir)
                         if any(p.startswith(".") for p in rel_path.split(os.sep)): continue
                         try:
                             with open(abs_path, "r", encoding="utf-8") as f:
                                 files.append({"path": rel_path, "content": f.read()})
                         except Exception: pass

        has_entry = False
        if files:
             for f in files:
                 path = f["path"]
                 content = f["content"]
                 if ".." in path or path.startswith("/"): continue
                 
                 # Path Normalization: Strip workspace/ prefix
                 if path.startswith("workspace/") or path.startswith("workspace\\"):
                     path = path[10:]
                 elif path.startswith("workspace") and (len(path) > 9 and path[9] in [os.sep, '/']):
                     path = path[10:]
                     
                 full_path = os.path.join(td, path)
                 os.makedirs(os.path.dirname(full_path), exist_ok=True)
                 with open(full_path, "w", encoding="utf-8") as fw:
                     fw.write(content)

        # Injected code override
        if code:
             path = os.path.join(td, "main.js")
             with open(path, "w", encoding="utf-8") as f:
                 f.write(code)
             has_entry = True
             
        # Determine entrypoint
        # Priority 1: Explicit target (example.py mode)
        effective_entrypoint = entrypoint or "main.js"
        found_entry = False
        
        listing = []
        for root, _, filenames in os.walk(td):
            for f in filenames:
                listing.append(os.path.relpath(os.path.join(root, f), td))

        if entrypoint and entrypoint in listing:
            effective_entrypoint = entrypoint
            found_entry = True

        # Priority 2: Workspace metadata
        if not found_entry and workspace and workspace.get("entrypoint"):
            ws_entry = workspace["entrypoint"]
            if ws_entry.startswith("workspace/") or ws_entry.startswith("workspace\\"):
                ws_entry = ws_entry[10:]
            if ws_entry in listing:
                effective_entrypoint = ws_entry
                found_entry = True
        
        # Priority 3: Auto-detection
        if not found_entry:
            if "index.js" in listing:
                 effective_entrypoint = "index.js"
            elif "main.js" in listing:
                 effective_entrypoint = "main.js"
        
        path = os.path.join(td, effective_entrypoint)
        if not os.path.exists(path):
             return ExecResult(ok=False, exit_code=2, duration_ms=0, stdout="", stderr=f"Entrypoint '{effective_entrypoint}' not found.", timed_out=False)

        cmd = ["node", path]
        env = os.environ.copy() # Inherit for node/npm
        env.update({
            "GIT_EDITOR": "true",
            "GIT_TERMINAL_PROMPT": "0",
        })

        try:
            p = subprocess.run(
                cmd,
                input=stdin.encode("utf-8") if stdin else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=td,
                env=env,
                timeout=max(0.1, timeout_ms / 1000.0),
            )
            dt = int((time.time() - t0) * 1000)
            return ExecResult(
                ok=(p.returncode == 0),
                exit_code=p.returncode,
                duration_ms=dt,
                stdout=p.stdout.decode("utf-8", errors="replace"),
                stderr=p.stderr.decode("utf-8", errors="replace"),
                timed_out=False,
                state=_capture_state(td)
            )
        except subprocess.TimeoutExpired as e:
            dt = int((time.time() - t0) * 1000)
            return ExecResult(
                ok=False, 
                exit_code=None, 
                duration_ms=dt, 
                stdout=(e.stdout or b"").decode("utf-8", errors="replace"), 
                stderr="[Timed out]", 
                timed_out=True,
                state=_capture_state(td)
            )


from typing import Optional, Dict, Any

def run_shell_local(code: str, stdin: str = "", timeout_ms: int = 30000,
                    workspace: Optional[Dict[str, Any]] = None, quest_slug: Optional[str] = None,
                    entrypoint: Optional[str] = None) -> ExecResult:
    """
    Run a shell script locally (in the backend process environment).
    Used for world-git quests — requires git binary in the backend image.
    Injects GIT_AUTHOR_NAME/EMAIL so commits work without global git config.
    """
    import tempfile, subprocess as sp
    t0 = time.time()

    with tempfile.TemporaryDirectory(prefix="evalforge-shell-") as td:
        # 1. Write workspace files
        files = workspace.get("files", []) if workspace else []
        for wf in files:
            rel = wf.get("path", "")
            if not rel or ".." in rel:
                continue
            full = os.path.join(td, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(wf.get("content", ""))

        # 2. Write the learner script (overrides workspace copy if present)
        ep = entrypoint or "task.sh"
        script_path = os.path.join(td, ep)
        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w", encoding="utf-8") as fh:
            fh.write(code)
        try:
            os.chmod(script_path, 0o755)
        except Exception:
            pass

        # 3. Build environment — inject git identity so commits don't fail
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": env.get("GIT_AUTHOR_NAME", "EvalForge"),
            "GIT_AUTHOR_EMAIL": env.get("GIT_AUTHOR_EMAIL", "evalforge@example.com"),
            "GIT_COMMITTER_NAME": env.get("GIT_COMMITTER_NAME", "EvalForge"),
            "GIT_COMMITTER_EMAIL": env.get("GIT_COMMITTER_EMAIL", "evalforge@example.com"),
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_EDITOR": "true",
            "HOME": td,  # isolate git global config
        })

        try:
            p = sp.run(
                ["sh", ep],
                input=stdin.encode("utf-8") if stdin else None,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                cwd=td,
                env=env,
                timeout=max(1.0, timeout_ms / 1000.0),
            )
            dt = int((time.time() - t0) * 1000)
            return ExecResult(
                ok=(p.returncode == 0),
                exit_code=p.returncode,
                duration_ms=dt,
                stdout=p.stdout.decode("utf-8", errors="replace"),
                stderr=p.stderr.decode("utf-8", errors="replace"),
                timed_out=False,
            )
        except sp.TimeoutExpired as e:
            dt = int((time.time() - t0) * 1000)
            out = (e.stdout or b"").decode("utf-8", errors="replace")
            err = (e.stderr or b"").decode("utf-8", errors="replace")
            return ExecResult(
                ok=False, exit_code=None, duration_ms=dt,
                stdout=out, stderr=err + "\n[Timed out]", timed_out=True,
            )


def run_code(language: str, code: str, stdin: str = "", timeout_ms: int = 2000, workspace: Optional[Dict[str, Any]] = None, mode: str = "run", entrypoint: Optional[str] = None, quest_slug: Optional[str] = None) -> ExecResult:
    """
    Dispatcher for code execution.
    - Python: Supports 'local' (dev) or 'docker'.
    - JS: Supports 'local' (dev) or 'docker'.
    - Shell: Runs locally (requires git binary — world-git quests).
    - Other: Requires 'docker'.
    """
    backend = os.getenv("EXECUTION_BACKEND", "local")

    # Shell runs locally always — docker runner can't write to /workspace as nobody user
    if language == "shell":
        return run_shell_local(code, stdin=stdin, timeout_ms=max(timeout_ms, 30000),
                               workspace=workspace, quest_slug=quest_slug, entrypoint=entrypoint)

    # Force docker for non-supported local languages or tests mode
    use_docker = (backend == "docker") or (language not in ["python", "javascript"]) or (mode == "tests")
    debug_log(f"DEBUG[code_runner.run_code]: lang={language} backend={backend} use_docker={use_docker}")

    if use_docker:
        from arcade_app.services.code_runner_docker import run_code_docker
        return run_code_docker(language, code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace, mode=mode, entrypoint=entrypoint, quest_slug=quest_slug)

    if language == "javascript":
        return run_javascript_local(code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace, quest_slug=quest_slug, entrypoint=entrypoint)

    return run_python_local(code, stdin=stdin, timeout_ms=timeout_ms, workspace=workspace, quest_slug=quest_slug, entrypoint=entrypoint)

# Alias for backward compatibility if needed, but we should switch callers
run_python = lambda c, s="", t=2000: run_code("python", c, s, t)
