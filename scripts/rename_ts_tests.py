import os

repo_root = "d:/EvalForge"
quests_dir = f"{repo_root}/docs/quests"

for item in os.listdir(quests_dir):
    if item.startswith("ts-"):
        grading_dir = f"{quests_dir}/{item}/grading/public"
        if os.path.exists(grading_dir):
            for f in os.listdir(grading_dir):
                if f.endswith(".public.test.mjs"):
                    old_path = f"{grading_dir}/{f}"
                    new_path = f"{grading_dir}/{f.replace('.mjs', '.ts')}"
                    try:
                        os.rename(old_path, new_path)
                        print(f"Renamed {old_path} -> {new_path}")
                    except FileExistsError:
                        print(f"Skipping {old_path} -> {new_path} (exists)")
                        # If exists, we can remove the old file to be clean
                        os.remove(old_path)
                        print(f"Removed old {old_path}")
