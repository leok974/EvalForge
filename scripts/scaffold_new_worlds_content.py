
import json
import os

def load_questpack(path):
    with open(path, 'r') as f:
        return json.load(f)

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created {path}")

DESCRIPTIONS = {
    # CLI
    "cli-ignition": "Learn the terminal mental model (command → output) and run your first safe commands confidently.",
    "cli-navigation": "Move between folders and build path intuition so you never feel “lost” in a repo again.",
    "cli-files-folders": "Manipulate files and directories using safe patterns that prevent accidental data loss.",
    "cli-globs-search": "Use wildcards and search tools to locate files and text quickly in real projects.",
    "cli-redirection": "Capture command output into files and logs without overwriting mistakes.",
    "cli-pipes": "Chain commands together to transform and summarize output like a pro.",
    "cli-env-vars": "Understand how tools and configs are discovered so your dev setup stops feeling magical.",
    "cli-exit-codes": "Make automation reliable by detecting failure and handling errors intentionally.",
    "cli-processes": "Inspect what’s running, stop stuck tasks, and understand the basics of process control.",
    "cli-scripting": "Write a tiny script that accepts args, handles failures, and behaves safely.",
    
    # React
    "react-ignition": "Render your first component and understand JSX as a readable UI syntax.",
    "react-props": "Pass data into components and build reusable UI blocks.",
    "react-state": "Add interactivity with state and understand why React re-renders.",
    "react-events": "Handle user input correctly with event handlers and controlled form fields.",
    "react-lists-keys": "Render collections without bugs by choosing stable keys and avoiding common list traps.",
    "react-effects": "Fetch data and manage side effects safely with dependency discipline.",
    "react-custom-hooks": "Extract shared logic into hooks to keep components clean and composable.",
    "react-context": "Avoid prop drilling and use context intentionally for app-level concerns.",
    "react-routing": "Build a simple multi-page app using routes and params.",
    "react-performance-basics": "Learn practical performance habits and when memoization helps (and hurts).",
}

TUTORIAL_SECTIONS = {
    # CLI
    "cli-ignition": [
        ("Outcome", "Run basic safe commands and interpret their output."),
        ("Core concepts", "terminal, command, stdout/stderr, working directory."),
        ("Mental model", "“Where am I?” + “What command am I running?” + “What did it print?”"),
        ("Walkthrough", "`pwd`, `ls`, `whoami` (or platform-safe equivalents) + reading output."),
        ("Practice", "list files, identify current folder, confirm a file exists."),
        ("Common pitfalls", "confusing output with errors, running commands in wrong folder."),
        ("Check yourself", "What does `pwd` tell you? What’s stdout vs stderr?"),
    ],
    "cli-navigation": [
        ("Outcome", "Move around confidently using relative/absolute paths."),
        ("Core concepts", "absolute vs relative, `..`, home dir, current dir."),
        ("Mental model", "“paths are addresses” and `cd` changes your viewpoint."),
        ("Walkthrough", "`cd`, `cd ..`, `cd ~`, navigating into a project folder."),
        ("Practice", "go to a folder, return, jump to home, re-enter by relative path."),
        ("Common pitfalls", "spaces in paths, assuming `cd` “opens” files."),
        ("Check yourself", "What’s the difference between `/` and `~`? When do you use `..`?"),
    ],
    "cli-files-folders": [
        ("Outcome", "Create/copy/move/delete with safe verification steps."),
        ("Core concepts", "mkdir, touch/new file, cp, mv, rm, recursive."),
        ("Mental model", "“copy makes two, move relocates, delete is permanent.”"),
        ("Walkthrough", "create a folder, create file, copy it, rename it, remove safely."),
        ("Practice", "make `sandbox/`, copy files, rename, delete only inside sandbox."),
        ("Common pitfalls", "`rm -rf` muscle memory, deleting wrong directory."),
        ("Check yourself", "When does `mv` rename vs move? What makes deletes dangerous?"),
    ],
    "cli-globs-search": [
        ("Outcome", "Find files and grep/search text quickly."),
        ("Core concepts", "glob patterns `* ? []`, search tools, match vs no match."),
        ("Mental model", "“globs match filenames; search matches file contents.”"),
        ("Walkthrough", "`ls *.md`, search for a string in a repo (tooling-agnostic)."),
        ("Practice", "find all `.json`, find where a slug appears, confirm hits."),
        ("Common pitfalls", "quoting globs, searching huge dirs, case sensitivity."),
        ("Check yourself", "What does `*` match? What’s the difference between file search and text search?"),
    ],
    "cli-redirection": [
        ("Outcome", "Save output to files and logs correctly."),
        ("Core concepts", "`>`, `>>`, stderr redirection, “overwrite vs append.”"),
        ("Mental model", "“a command prints; redirection routes that print somewhere else.”"),
        ("Walkthrough", "write output to `out.txt`, append additional lines, capture errors."),
        ("Practice", "generate a log, append timestamps, confirm file contents."),
        ("Common pitfalls", "overwriting accidentally, forgetting stderr exists."),
        ("Check yourself", "What does `>` do vs `>>`? Why might stderr not appear in your file?"),
    ],
    "cli-pipes": [
        ("Outcome", "Combine commands to transform output."),
        ("Core concepts", "pipe `|`, stdin/stdout, filters, composition."),
        ("Mental model", "“left command produces; right command consumes.”"),
        ("Walkthrough", "list → filter → count/summarize (use platform-available examples)."),
        ("Practice", "pipe search results into a counter or sorter."),
        ("Common pitfalls", "piping binary output, assuming pipes keep formatting."),
        ("Check yourself", "What flows through a pipe? Why do filters make scripts shorter?"),
    ],
    "cli-env-vars": [
        ("Outcome", "Inspect/set env vars and understand PATH lookup."),
        ("Core concepts", "env var, process env, PATH, config via env."),
        ("Mental model", "“env vars are per-process settings; PATH is the tool search list.”"),
        ("Walkthrough", "print an env var, set one temporarily, verify it changes behavior."),
        ("Practice", "set a dummy var and read it; locate a command via PATH."),
        ("Common pitfalls", "permanent vs temporary vars, confusing shell config vs env."),
        ("Check yourself", "Why does restarting a terminal “lose” temporary vars? What is PATH?"),
    ],
    "cli-exit-codes": [
        ("Outcome", "Detect success/failure and branch behavior."),
        ("Core concepts", "exit code 0/non-zero, short-circuit operators, failure modes."),
        ("Mental model", "“programs report success with a number, not with text.”"),
        ("Walkthrough", "run a command that fails, inspect code, handle conditionally."),
        ("Practice", "write a tiny “check then run” sequence."),
        ("Common pitfalls", "relying on printed text, swallowing errors."),
        ("Check yourself", "What does exit code 0 mean? Why is “no output” not necessarily success?"),
    ],
    "cli-processes": [
        ("Outcome", "Inspect and stop running processes safely."),
        ("Core concepts", "PID, foreground/background, kill, signals."),
        ("Mental model", "“processes are running programs; signals request behavior.”"),
        ("Walkthrough", "start a long-running task, find it, stop it cleanly."),
        ("Practice", "identify a process by name and end it safely."),
        ("Common pitfalls", "killing the wrong PID, force-killing too early."),
        ("Check yourself", "What’s the difference between a gentle stop and a forced kill?"),
    ],
    "cli-scripting": [
        ("Outcome", "Write a tiny script with args and safe defaults."),
        ("Core concepts", "shebang (optional), args, quoting, exit codes, `set -e` style safety."),
        ("Mental model", "“scripts are just commands saved in a file.”"),
        ("Walkthrough", "script that takes a filename, checks it, prints a summary."),
        ("Practice", "add an option flag, handle missing arg, return proper exit code."),
        ("Common pitfalls", "unquoted variables, spaces in paths, ignoring failures."),
        ("Check yourself", "Why do quotes matter? How do you signal failure to CI?"),
    ],

    # React
    "react-ignition": [
        ("Outcome", "Build and render a component using JSX."),
        ("Core concepts", "component, JSX, render tree."),
        ("Mental model", "“UI is a function of state/props.”"),
        ("Walkthrough", "create `App`, render a header + paragraph, reuse a small component."),
        ("Practice", "build a `Card` component and render 3 cards."),
        ("Common pitfalls", "forgetting `return`, invalid JSX nesting, missing keys (preview)."),
        ("Check yourself", "What does JSX compile to? Why is React declarative?"),
    ],
    "react-props": [
        ("Outcome", "Pass props and render dynamic UI."),
        ("Core concepts", "props, children, composition."),
        ("Mental model", "“props are read-only inputs.”"),
        ("Walkthrough", "`UserCard({ name, role })`, `children` slot."),
        ("Practice", "create a `Button` with `variant` prop and reuse it."),
        ("Common pitfalls", "mutating props, too many props vs composition."),
        ("Check yourself", "When do you use `children` vs a custom prop?"),
    ],
    "react-state": [
        ("Outcome", "Add state-driven interactivity."),
        ("Core concepts", "state, setter, rerender, immutability."),
        ("Mental model", "“setState schedules a rerender with new values.”"),
        ("Walkthrough", "toggle, counter, derived display text."),
        ("Practice", "build a small “expand/collapse” panel."),
        ("Common pitfalls", "direct mutation, stale reads, async mental model mistakes."),
        ("Check yourself", "Why must state updates be immutable? What triggers rerenders?"),
    ],
    "react-events": [
        ("Outcome", "Handle events and build a controlled form."),
        ("Core concepts", "events, controlled input, onSubmit."),
        ("Mental model", "“input value lives in state; DOM reflects it.”"),
        ("Walkthrough", "text input + checkbox + submit handler."),
        ("Practice", "validation message when input is empty."),
        ("Common pitfalls", "uncontrolled/controlled mismatch, forgetting `preventDefault`."),
        ("Check yourself", "What makes an input “controlled”? Why preventDefault?"),
    ],
    "react-lists-keys": [
        ("Outcome", "Render arrays reliably and choose correct keys."),
        ("Core concepts", "list rendering, keys, reconciliation."),
        ("Mental model", "“keys identify items across renders.”"),
        ("Walkthrough", "map over data, use stable id keys, reorder scenario."),
        ("Practice", "render a todo list and allow removing items."),
        ("Common pitfalls", "using index as key, generating random keys."),
        ("Check yourself", "When is index-key acceptable? What breaks when keys are unstable?"),
    ],
    "react-effects": [
        ("Outcome", "Fetch data and manage side effects safely."),
        ("Core concepts", "`useEffect`, deps array, cleanup."),
        ("Mental model", "“effects run after paint; deps control when.”"),
        ("Walkthrough", "fetch on mount, loading/error states, cleanup pattern."),
        ("Practice", "refetch when a parameter changes."),
        ("Common pitfalls", "missing deps, infinite loops, stale closures."),
        ("Check yourself", "What belongs in deps? When do you need cleanup?"),
    ],
    "react-custom-hooks": [
        ("Outcome", "Extract logic into a hook and reuse it."),
        ("Core concepts", "hook rules, composition, reuse."),
        ("Mental model", "“hooks are reusable stateful functions.”"),
        ("Walkthrough", "`useToggle`, `useDebounce` (simple)."),
        ("Practice", "create `useLocalStorageState` (basic)."),
        ("Common pitfalls", "calling hooks conditionally, leaky abstractions."),
        ("Check yourself", "What are the Rules of Hooks? Why do they exist?"),
    ],
    "react-context": [
        ("Outcome", "Share small global state via context."),
        ("Core concepts", "provider, consumer, value identity."),
        ("Mental model", "“context is implicit props for a subtree.”"),
        ("Walkthrough", "theme context or auth-lite context, consuming in children."),
        ("Practice", "toggle theme and persist in state."),
        ("Common pitfalls", "overusing context, rerender storms, missing memoization."),
        ("Check yourself", "When is context appropriate vs props? What causes rerenders?"),
    ],
    "react-routing": [
        ("Outcome", "Build multi-page navigation with params."),
        ("Core concepts", "routes, params, links, layouts."),
        ("Mental model", "“URL selects which component tree is shown.”"),
        ("Walkthrough", "list page → detail page via param."),
        ("Practice", "add a “Not Found” route and a nested layout."),
        ("Common pitfalls", "mismatched paths, forgetting to handle missing params."),
        ("Check yourself", "Why are routes a state mechanism? What is a param?"),
    ],
    "react-performance-basics": [
        ("Outcome", "Diagnose unnecessary rerenders and apply basic fixes."),
        ("Core concepts", "rerender triggers, memoization, referential equality."),
        ("Mental model", "“new object/function props can trigger rerenders.”"),
        ("Walkthrough", "use `memo`, `useMemo`, `useCallback` in one small scenario."),
        ("Practice", "optimize a list render without premature complexity."),
        ("Common pitfalls", "memo everywhere, optimizing before measuring."),
        ("Check yourself", "When does memoization help? What’s the cost of overusing it?"),
    ],
}

def generate_quest_files(pack_path):
    pack = load_questpack(pack_path)
    world_id = pack['world_id']
    track_id = pack['track_id']
    language = "bash" if "cli" in world_id else "typescript"
    
    for quest in pack['quests']:
        slug = quest['slug']
        title = quest['title']
        order = quest['order']
        
        desc = DESCRIPTIONS.get(slug, "Description pending.")
        sections = TUTORIAL_SECTIONS.get(slug, [])
        
        # 1. quest.json
        quest_data = {
            "slug": slug,
            "title": title,
            "short_description": desc,
            "world_id": world_id,
            "track_id": track_id,
            "order_index": order,
            "base_xp_reward": 50,
            "language": language
        }
        
        q_dir = os.path.join("docs", "quests", slug)
        write_file(os.path.join(q_dir, "quest.json"), json.dumps(quest_data, indent=4))
        
        # 2. tutorial.md
        md_content = f"# {title}\n\n"
        for section, body in sections:
            md_content += f"## {section}\n\n{body}\n\n"
            
        write_file(os.path.join(q_dir, "tutorial.md"), md_content)

def main():
    generate_quest_files("data/questpacks/cli_core.json")
    generate_quest_files("data/questpacks/react_core.json")

if __name__ == "__main__":
    main()
