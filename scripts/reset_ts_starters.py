import os
import re

quests = [
    "ts-vars",
    "ts-types",
    "ts-control",
    "ts-arrays",
    "ts-objects",
    "ts-functions",
    "ts-interfaces",
    "ts-generics",
    "ts-modules"
]

repo_root = "d:/EvalForge"

def create_starter(content):
    # Remove function bodies
    # Heuristic: replace { ... } block of export function with { throw new Error("TODO"); }
    # This is regex-heavy and fragile, but okay for this batch.
    
    # Matches export function foo(...): Type { ... }
    # We want to keep the signature.
    
    # Simple state machine cleaner might be safer.
    lines = content.splitlines()
    new_lines = []
    skip = False
    
    # Actually, let's use a simpler heuristic for now:
    # If it's a function, replace the body with throw.
    # If it's a variable (const), leave it or replace value? 
    # ts-vars has `export const greeting = ...;` -> should probably be `export const greeting = "TODO";`
    
    # Given I can't easily parse TS, I will try to be conservative.
    # I will replace `return { ... };` with `throw new Error("TODO");` inside functions?
    
    # Better: just look for `export function ... {` and replace until `}`? Nested braces make this hard.
    
    # Alternative: Just write a loop that reads a few lines and manually creates them? No, 10 files.
    
    # I'll try to just blank out the obvious returns.
    return content

    # WAIT. I am an agent. I can read the files, LLM-process them, and write them back.
    # But I can't do that easily in a python script I write blindly.
    
    # Reset strategy: I will just use the script to list the files, and I will use `replace_file_content` via the LLM (me) to edit them?
    # No, that consumes 9 turns.
    
    # Let's try to make a "best effort" stripper in Python.
    
    # Pattern: export function name(args): Type { ... }
    # Pattern: export const name: Type = { ... };
    
    pass

# Update: I will just overwrite them with a valid generic starter that likely compiles but fails.
# Most quests obey `task.ts` convention.
# But `ts-vars` exports consts. `ts-functions` exports matchers.

# Let's read the solution, and if it's too hard to strip, I'll just leave it and accept that student mode passes for now?
# NO, "Training Grade" requires valid processing.

# I will write a script that essentially:
# 1. Reads the solution file.
# 2. Uses regex to replace `return ...;` with `throw new Error("TODO");`
# 3. Uses regex to replace `export const x = ...;` with `export const x = ...; // TODO` (maybe manually nulling it?)

# Let's try this:
# Just blindly replace the `workspace/task.ts` with a file that says "TODO" but compiles?
# Typescript requires the exports to exist.

# I will iterate through them and validly break them.
# ts-vars:
# export const greeting = "TODO" as any;
# export const config: any = {};

# ts-ignition (DONE)

# script logic:
for slug in quests:
    sol_path = f"{repo_root}/solutions/{slug}/task.ts"
    ws_path = f"{repo_root}/docs/quests/{slug}/workspace/task.ts"
    
    if not os.path.exists(sol_path):
        continue
        
    with open(sol_path, "r", encoding="utf-8") as f:
        src = f.read()
    
    # Naive replacements
    # 1. Replace return object literals
    src = re.sub(r'return\s+\{[^;]+?\};', 'throw new Error("Not implemented");', src, flags=re.DOTALL)
    # 2. Replace simple returns
    src = re.sub(r'return\s+[^;]+;', 'throw new Error("Not implemented");', src)
    
    # 3. For consts, replace "System Online" strings etc
    src = src.replace('"System Online"', '"TODO"')
    src = src.replace('true', 'false')
    src = src.replace('42', '0')
    
    # This is very rough, but might work for student mode failure.
    
    with open(ws_path, "w", encoding="utf-8") as f:
        f.write(src)
        
    print(f"Reset {slug}")
