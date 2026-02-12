import os

repo_root = "d:/EvalForge"
quests_dir = f"{repo_root}/docs/quests"

for item in os.listdir(quests_dir):
    if item.startswith("ts-"):
        grading_dir = f"{quests_dir}/{item}/grading/public"
        if os.path.exists(grading_dir):
            for f in os.listdir(grading_dir):
                if f.endswith(".public.test.mjs"):
                    full_path = f"{grading_dir}/{f}"
                    os.remove(full_path)
                    print(f"Deleted {full_path}")
