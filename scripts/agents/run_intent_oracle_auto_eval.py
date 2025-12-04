import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(cmd, cwd=None, env=None, check=True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )
    if check and proc.returncode != 0:
        msg = proc.stderr.strip() or proc.stdout.strip()
        raise RuntimeError(f"Command failed ({cmd}): {msg}")
    return proc


def main() -> int:
    """
    Auto-eval pipeline:

    - Reads configuration from environment:
        REPO_URL (required)
        REPO_BRANCH (optional)
        PLANNER_REL_PATH (default: 'scripts/agents/candidate_planner.py')
        PLANNER_GENERATOR (optional shell command with {PLANNER_REL_PATH} placeholder)

    - Clones the repo into a temp dir.
    - Optionally runs generator command to produce candidate planner.
    - Calls run_intent_oracle_eval.py with the absolute planner path.
    - Prints the JSON output from that script to stdout.
    """
    repo_url = os.environ.get("REPO_URL")
    if not repo_url:
        print("REPO_URL is required", file=sys.stderr)
        return 1

    repo_branch = os.environ.get("REPO_BRANCH") or ""
    planner_rel = os.environ.get("PLANNER_REL_PATH") or "scripts/agents/candidate_planner.py"
    generator_cmd_tpl = os.environ.get("PLANNER_GENERATOR") or ""

    # Where run_intent_oracle_eval.py lives (EvalForge repo root)
    project_root = Path(__file__).resolve().parents[2]  # adjust if layout differs
    eval_script = project_root / "scripts" / "agents" / "run_intent_oracle_eval.py"
    if not eval_script.is_file():
        print(f"Eval script not found at {eval_script}", file=sys.stderr)
        return 1

    # Env must already contain EVALFORGE_BASE_URL and EVALFORGE_API_TOKEN
    eval_env = os.environ.copy()
    if "EVALFORGE_BASE_URL" not in eval_env or "EVALFORGE_API_TOKEN" not in eval_env:
        print("EVALFORGE_BASE_URL and EVALFORGE_API_TOKEN must be set", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # 1) Clone repo
        _run(["git", "clone", repo_url, "."], cwd=tmp_path, env=eval_env)
        if repo_branch:
            _run(["git", "checkout", repo_branch], cwd=tmp_path, env=eval_env)

        # 2) Optionally run planner generator
        planner_rel_path = Path(planner_rel)
        if generator_cmd_tpl:
            gen_cmd = generator_cmd_tpl.format(PLANNER_REL_PATH=str(planner_rel_path))
            # Run via shell so users can pass complex commands
            # Note: shell=True is generally unsafe but this is an internal dev tool
            # For better safety we might want to parse the command
            subprocess.run(gen_cmd, cwd=tmp_path, env=eval_env, check=True, shell=True)

        candidate_abs = tmp_path / planner_rel_path
        if not candidate_abs.is_file():
            print(f"Planner file not found at {candidate_abs}", file=sys.stderr)
            return 1

        # 3) Run the existing eval script, passing absolute planner path
        proc = subprocess.run(
            [sys.executable, str(eval_script), str(candidate_abs)],
            cwd=project_root,
            env=eval_env,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            msg = proc.stderr.strip() or proc.stdout.strip()
            print(f"run_intent_oracle_eval.py failed: {msg}", file=sys.stderr)
            return proc.returncode

        # Validate JSON and echo to stdout
        stdout = proc.stdout.strip()
        try:
            parsed = json.loads(stdout)
        except json.JSONDecodeError as exc:
            print(f"Eval script output was not valid JSON: {exc}", file=sys.stderr)
            return 1

        print(json.dumps(parsed))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
