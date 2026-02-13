import json
import os
import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = ROOT / "data" / "quests"
DOCS_QUESTS = ROOT / "docs" / "quests"
PACKS_DIR = ROOT / "data" / "questpacks"

def run_cmd(args):
    try:
        res = subprocess.run(args, capture_output=True, text=True, check=False, shell=True)
        return res.stdout.strip()
    except Exception as e:
        return str(e)

def get_repo_context():
    node_v = run_cmd("node -v")
    npm_v = run_cmd("npm -v")
    
    pkg_path = ROOT / "package.json"
    pkg_data = {}
    if pkg_path.exists():
        pkg_data = json.loads(pkg_path.read_text(encoding="utf-8"))
    
    deps = pkg_data.get("dependencies", {})
    dev_deps = pkg_data.get("devDependencies", {})
    
    interesting = ["jsdom", "linkedom", "cheerio", "happy-dom", "parse5"]
    installed_interesting = {}
    for i in interesting:
        installed_interesting[i] = (i in deps) or (i in dev_deps)
        
    shared_data = []
    shared_dir = ROOT / "data" / "_shared"
    if shared_dir.exists():
        shared_data = [f.name for f in shared_dir.glob("*web*")]
        if (shared_dir / "node_test_helpers.mjs").exists():
            shared_data.append("node_test_helpers.mjs")
            
    shared_quests = []
    q_shared_dir = ROOT / "data" / "quests" / "_shared"
    if q_shared_dir.exists():
        shared_quests = [f.name for f in q_shared_dir.glob("*")]

    # Check test runners usage (heuristic)
    uses_node_test = "node --test" in (pkg_data.get("scripts", {}).get("test:web", "") or "")
    uses_playwright = "playwright" in (pkg_data.get("scripts", {}).get("test:e2e", "") or "")

    return {
        "node_version": node_v,
        "npm_version": npm_v,
        "package_json_partial": {
            "dependencies": deps,
            "devDependencies": dev_deps
        },
        "target_deps_installed": installed_interesting,
        "data_shared_files": shared_data,
        "data_quests_shared_files": shared_quests,
        "test_runner_heuristics": {
            "uses_node_test": uses_node_test,
            "uses_playwright": uses_playwright
        }
    }

def load_pack(filename):
    p = PACKS_DIR / filename
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        return None

def extract_slugs(pack_data):
    slugs = []
    if not pack_data: return slugs
    
    # Handle older 'quests' list
    items = pack_data
    if isinstance(pack_data, dict):
        if "quests" in pack_data:
            items = pack_data["quests"]
        elif "entries" in pack_data:
            items = pack_data["entries"]
            
    if not isinstance(items, list):
        return []

    for it in items:
        if isinstance(it, str):
            slugs.append(it)
        elif isinstance(it, dict):
            if "slug" in it:
                slugs.append(it["slug"])
            elif "quest_path" in it:
                slugs.append(it["quest_path"].replace("\\", "/").split("/")[-1])
            elif "questPath" in it:
                slugs.append(it["questPath"].replace("\\", "/").split("/")[-1])
    return slugs

def check_alignment(slugs):
    docs_only = []
    data_only = [] # Harder to verify 'data_only' without scanning all data/quests
    missing_everywhere = []
    
    for s in slugs:
        has_data = (DATA_QUESTS / s).exists()
        has_docs = (DOCS_QUESTS / s).exists()
        
        if has_docs and not has_data:
            docs_only.append(s)
        elif has_data and not has_docs:
            data_only.append(s)
        elif not has_data and not has_docs:
            missing_everywhere.append(s)
            
    return {
        "docs_only_slugs": docs_only,
        "data_only_slugs": data_only, # Misnomer in loop logic, actually these are aligned if both exist
        "missing_everywhere": missing_everywhere
    }

def get_grading_status(slugs):
    res = []
    for s in slugs:
        q = DATA_QUESTS / s
        
        ws_files = []
        if (q / "workspace").exists():
            ws_files = [f.name for f in (q / "workspace").glob("*")]
            
        public_tests = []
        if (q / "grading" / "public").exists():
            public_tests = [f.name for f in (q / "grading" / "public").glob("*test*")]
            
        res.append({
            "slug": s,
            "has_workspace": (q / "workspace").exists(),
            "has_grading_public": (q / "grading" / "public").exists(),
            "has_grading_solutions": (q / "grading" / "solutions").exists(),
            "public_tests": public_tests,
            "workspace_files": ws_files
        })
    return res

def get_sample(slug):
    q = DATA_QUESTS / slug
    if not q.exists():
        q = DOCS_QUESTS / slug # Fallback if only in docs
        if not q.exists():
            return None
            
    # Tree
    tree = []
    for r, ds, fs in os.walk(q):
        rel = Path(r).relative_to(q)
        for f in fs:
            tree.append(str(rel / f).replace("\\", "/"))
            
    readme = ""
    readme_path = q / "workspace" / "README.md"
    if not readme_path.exists():
        # Try docs path
        readme_path = DOCS_QUESTS / slug / "README.md"
        
    if readme_path.exists():
        readme = readme_path.read_text(encoding="utf-8", errors="ignore")
        
    # Heuristic for learner file
    learner_files = {}
    for f in ["index.html", "style.css", "styles.css", "task.html", "task.css"]:
        fp = q / "workspace" / f
        if fp.exists():
            learner_files[f] = fp.read_text(encoding="utf-8", errors="ignore")

    public_tests_content = {}
    if (q / "grading" / "public").exists():
         for f in (q / "grading" / "public").glob("*"):
             if f.is_file():
                 public_tests_content[f.name] = f.read_text(encoding="utf-8", errors="ignore")

    return {
        "slug": slug,
        "path": str(q),
        "tree": tree,
        "readme_content": readme,
        "learner_files_content": learner_files,
        "public_tests_content": public_tests_content
    }

def check_runner_compat(pack_path, mode="student"):
    # generic fallback run
    cmd = f"node scripts/run_world_public_tests.mjs --questpack {pack_path} --mode {mode}"
    out = run_cmd(cmd)
    return out

def main():
    # 1. Packs
    html_pack = load_pack("web_html_core.json")
    css_pack = load_pack("web_css_core.json")
    
    html_slugs = extract_slugs(html_pack)
    css_slugs = extract_slugs(css_pack)
    
    # 2. Alignment
    html_align = check_alignment(html_slugs)
    css_align = check_alignment(css_slugs)
    
    # 3. Grading
    html_grading = get_grading_status(html_slugs)
    css_grading = get_grading_status(css_slugs)
    
    # 4. Samples
    html_sample_slug = html_slugs[0] if html_slugs else "web-html-ignition"
    css_sample_slug = css_slugs[0] if css_slugs else "web-css-ignition"
    
    html_sample = get_sample(html_sample_slug)
    css_sample = get_sample(css_sample_slug)
    
    # 5. Runner
    runner_out_html = check_runner_compat("data/questpacks/web_html_core.json")
    
    dump = {
        "repo_context": get_repo_context(),
        "web_world": {
            "html_slugs_count": len(html_slugs),
            "css_slugs_count": len(css_slugs)
        },
        "html_pack": {
            "raw": html_pack,
            "slugs": html_slugs,
            "alignment": html_align,
            "grading": html_grading
        },
        "css_pack": {
            "raw": css_pack,
            "slugs": css_slugs,
            "alignment": css_align,
            "grading": css_grading
        },
        "one_quest_samples": {
            "html": html_sample,
            "css": css_sample
        },
        "runner_compat": {
            "run_world_public_tests_mjs_output": runner_out_html,
            "analysis": "Runner falls back to generic loop. Fails if no public tests found. No mode swap logic for HTML/CSS files detected."
        },
        "blockers": [
            "No DOM parser (jsdom/cheerio) installed",
            "Unified runner lacks Web dispatch logic",
            "Unified runner generic loop assumes task.sh/.mjs, not index.html/styles.css"
        ],
        "recommendations": "Install jsdom (robust) or cheerio (light). Update runner to swap index.html/styles.css. Create scaffold script."
    }
    
    print(json.dumps({"web_world_context_dump": dump}, indent=2))

if __name__ == "__main__":
    main()
