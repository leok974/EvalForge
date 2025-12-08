from pathlib import Path

path = Path("docs/senior_tier_content.json")
lines = path.read_text(encoding="utf-8").splitlines()

# We want to keep lines up to 1297.
# 1297 lines means index 0 to 1296.
# Let's verify line 1297 content (index 1296).
limit = 1297
print(f"Line {limit}: {lines[limit-1]}")

clean_lines = lines[:limit]
print(f"Truncating to {len(clean_lines)} lines.")

path.write_text("\n".join(clean_lines), encoding="utf-8")
print("Fixed.")
