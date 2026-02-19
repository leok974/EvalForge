import shutil
from pathlib import Path

slugs = [
    "python-functions-contracts",
    "python-file-io-safe",
    "python-dicts-lists-transform",
    "python-cli-args",
    "python-oop-mini",
    "python-boss-csv-report"
]

base = Path("data/quests")

for slug in slugs:
    qdir = base / slug
    if not qdir.exists():
        print(f"Skipping {slug}, not found")
        continue
        
    # 1. Move Tests: workspace/tests/* -> grading/public/*
    ws_tests = qdir / "workspace/tests"
    grading_public = qdir / "grading/public"
    grading_public.mkdir(parents=True, exist_ok=True)
    
    if ws_tests.exists():
        for f in ws_tests.glob("*"):
            if f.is_file():
                shutil.move(str(f), str(grading_public / f.name))
        shutil.rmtree(ws_tests)
        print(f"Moved tests for {slug}")
        
    # 2. Move Solution: solution/* -> grading/solutions/*
    old_sol = qdir / "solution"
    grading_sol = qdir / "grading/solutions"
    grading_sol.mkdir(parents=True, exist_ok=True)
    
    if old_sol.exists():
        for f in old_sol.glob("*"):
            if f.is_file():
                shutil.move(str(f), str(grading_sol / f.name))
        shutil.rmtree(old_sol)
        print(f"Moved solution for {slug}")
