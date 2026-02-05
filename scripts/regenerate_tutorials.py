import os
import glob
from pathlib import Path

# New Template Logic (Duplicate from world_backfill_tutorials.py)
def generate_new_tutorial_content(slug):
    title = slug.replace("-", " ").title()
    return f"""## {title}

> [!NOTE]
> **What you'll build:** Practice {title.lower()} concepts in a real-world scenario.

---

## 1) What You'll Build
In this quest, you'll work with {title.lower()} to practice core concepts.

## 2) The Concept in 30 Seconds
{title} demonstrates fundamental programming patterns used in real-world applications.

## 3) Key Terms
- **term 1**
- **term 2**
(See Codex for full definitions)

---

## 4) Step-by-Step Walkthrough

### **Setup**
- Review the starting code
- Identify the input and expected output

### **Implementation**
- Follow the objectives
- Write your logic in the editor

### **Testing**
- Click **Run** to verify
- Check different input cases

---

## 5) Example Implementation
```python
# Example logic
def example():
    pass
```

---

## 6) Common Pitfalls

> [!WARNING]
>
> * Not reading error messages
> * Missing edge case handling
> * Syntax errors

---

## 7) Check Yourself

* [ ] Does the code run?
* [ ] Did you match the expected output?
* [ ] Did you handle edge cases?
"""

def main():
    root_dir = os.path.join(os.getcwd(), "docs", "quests")
    print(f"Scanning {root_dir}...")
    
    files = glob.glob(os.path.join(root_dir, "*", "tutorial.md"))
    print(f"Found {len(files)} tutorial files.")
    
    updated_count = 0
    skipeed_count = 0
    
    for file_path in files:
        slug = Path(file_path).parent.name
        
        # Read content to check if it matches old patterns
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Heuristics for "Legacy Stub"
        is_old_stub = False
        if "## 1. What You'll Build" in content:
            is_old_stub = True
        elif "## Outcome" in content:
            is_old_stub = True
        elif "# Git Init Clone" in content: # specific check from example
             is_old_stub = True
             
        # HEURISTIC: If it doesn't have the new Alert style, update it?
        if "> [!NOTE]" not in content:
            is_old_stub = True
            
        if is_old_stub:
            print(f"♻️  Regenerating: {slug}")
            new_content = generate_new_tutorial_content(slug)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated_count += 1
        else:
            print(f"⏭️  Skipping (Already updated or Custom): {slug}")
            skipeed_count += 1
            
    print(f"\nDone! Updated: {updated_count}, Skipped: {skipeed_count}")

if __name__ == "__main__":
    main()
