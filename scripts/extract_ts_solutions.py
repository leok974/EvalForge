import os
import shutil

quests = [
    "ts-ignition",
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

for slug in quests:
    ws_path = f"{repo_root}/docs/quests/{slug}/workspace/task.ts"
    sol_dir = f"{repo_root}/solutions/{slug}"
    sol_path = f"{sol_dir}/task.ts"

    # Ensure solution dir exists
    os.makedirs(sol_dir, exist_ok=True)

    # Read current content (solution)
    if os.path.exists(ws_path):
        with open(ws_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Write to solution file
        with open(sol_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Extracted solution for {slug}")

        # Create starter stub
        # We need to preserve imports/types but make the function fail or return dummy
        # This is hard to do generically 100% correct without parsing TS.
        # But we can try to guess based on structure, or just leave a generic TODO.
        
        # Simple heuristic: keep imports and type definitions. 
        # Replace function bodies with throw new Error("TODO").
        
        lines = content.splitlines()
        new_lines = []
        in_func = False
        brace_count = 0
        
        # Actually, let's just use a simpler approach:
        # If we see `export function`, we keep the signature and replace body.
        # This is risky. 
        # New plan: Just keep the file as is for now in workspace (so verification works)
        # AND copy to solution.
        # THEN manually edit the workspace file to be a starter?
        # A script cannot reliably generate a good starter from a solution without context.
        
        # BUT, the user wants me to be an agent.
        # "Agentic Mode": I should probably inspect them or make a best effort.
        # For now, I will just COPY the solution to the solution dir.
        # I will NOT overwrite the workspace file yet, so I can verify the runner works with the solution in place.
        # Then I will replace them one by one or via another tool call.
    else:
        print(f"Warning: No task.ts found for {slug}")
