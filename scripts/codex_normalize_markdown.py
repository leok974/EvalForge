
import os
import re
import argparse

def normalize_codex_file(filepath, dry_run=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Infer Metadata if missing Frontmatter
    has_frontmatter = content.strip().startswith('---')
    metadata = {}
    body = content
    
    if not has_frontmatter:
        lines = content.split('\n')
        new_lines = []
        in_header = True
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                if in_header and i > 0: in_header = False
            
            if in_header and i < 10 and ':' in stripped:
                key, val = stripped.split(':', 1)
                key = key.strip().lower()
                val = val.strip()
                if key in ['title', 'id', 'world', 'section', 'tags', 'level', 'related']:
                    # Parse array like string "[a, b]"
                    if val.startswith('[') and val.endswith(']'):
                         # Very basic check, assume it is valid yaml-ish
                         pass
                    metadata[key] = val
                else:
                    in_header = False
                    new_lines.append(line)
            else:
                in_header = False
                new_lines.append(line)
        
        body = '\n'.join(new_lines).strip()
    
    # 2. Add Frontmatter if we extracted metadata or if it was missing
    if not has_frontmatter and metadata:
        fm_lines = ["---"]
        for k, v in metadata.items():
            fm_lines.append(f"{k}: {v}")
        fm_lines.append("---\n")
        body = '\n'.join(fm_lines) + body

    current_content = body if not has_frontmatter else content

    # 3. Detect "Example" section without fences
    # Regex look for: ## Example (or similar) followed by non-fenced code
    # This is hard with regex alone because of multiline.
    # We will iterate lines statefully.
    
    lines = current_content.split('\n')
    processed_lines = []
    
    in_code_block = False
    in_example_section = False
    buffer = []
    
    # Simple heuristic:
    # If we see "## Example", we enter "example mode".
    # In example mode, if we see code-like lines indentation or keywords, and NO fencing, we wrap it.
    
    # Better approach from user plan:
    # "Detects “Example” section... If there is no fenced code block but it sees a run of code-ish lines... Wraps that run"
    
    # Let's try to identify blocks of code.
    # Code indicators: indentation, def, class, import, function, const, let, var, echo, $ 
    
    # Simplified State Machine
    # State: NORMAL -> EXAMPLE_SECTION -> POTENTIAL_CODE -> WRAPPING
    
    # Iterate
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Heading detection
        if stripped.startswith('#'):
            if 'example' in stripped.lower():
                in_example_section = True
            else:
                in_example_section = False
            processed_lines.append(line)
            i += 1
            continue
            
        if stripped.startswith('```'):
            # Already fenced
            processed_lines.append(line)
            # Skip until end of fence to avoid processing inside
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                processed_lines.append(lines[i])
                i += 1
            if i < len(lines): processed_lines.append(lines[i]) # The closing fence
            i += 1
            continue

        if in_example_section and stripped:
            # Check for code start
            is_code = False
            # Hardcoded heuristics for common languages in Codex (Python, TS, SQL, Shell)
            code_keywords = ['def ', 'class ', 'import ', 'from ', 'async ', 'await ', 
                             'function ', 'const ', 'let ', 'var ', 'console.', 
                             'SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ', 'CREATE ', 
                             '$ ', 'echo ', 'pip ', 'npm ', 'docker ']
            
            if (any(stripped.startswith(kw) for kw in code_keywords) or 
                (line.startswith('    ') and stripped) or # 4 space indent
                (stripped.endswith(';') or stripped.endswith('{') or stripped.endswith('}'))):
                is_code = True
            
            if is_code:
                # Start collecting code lines
                code_buffer = [line]
                
                # Look ahead
                j = i + 1
                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.strip()
                    
                    if next_stripped.startswith('```') or (next_stripped.startswith('#') and ' ' in next_stripped):
                        break # End of code block by fence or header
                    
                    # Heuristic: Allow empty lines in code
                    if not next_stripped:
                        code_buffer.append(next_line)
                        j += 1
                        continue
                        
                    # Stop if it looks like prose txt (starts with Capital letter and typically no code symbols?)
                    # Very risky. Let's assume Example section is mostly code.
                    # Or check indent?
                    
                    code_buffer.append(next_line)
                    j += 1
                
                # Trim trailing empty lines from buffer
                while code_buffer and not code_buffer[-1].strip():
                    j -= 1
                    code_buffer.pop()

                # Infer Language
                lang = 'txt'
                # Check metadata world
                world = metadata.get('world', '')
                if 'python' in world or any(l.strip().startswith(('def ', 'import ', 'class ')) for l in code_buffer):
                    lang = 'python'
                elif 'typescript' in world or 'react' in world or any(l.strip().startswith(('const ', 'let ', 'function ')) for l in code_buffer):
                    lang = 'typescript'
                elif 'sql' in world or any(l.strip().upper().startswith(('SELECT', 'INSERT')) for l in code_buffer):
                    lang = 'sql'
                elif 'shell' in world or any(l.strip().startswith(('$', 'echo', 'docker')) for l in code_buffer):
                    lang = 'bash'
                
                # Wrap
                processed_lines.append(f"```{lang}")
                processed_lines.extend(code_buffer)
                processed_lines.append("```")
                
                i = j
                continue

        processed_lines.append(line)
        i += 1

    final_content = '\n'.join(processed_lines)
    
    if final_content != original_content:
        print(f"Modifying {filepath}")
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(final_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--path', default='d:/EvalForge/data/codex')
    args = parser.parse_args()

    count = 0
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                if normalize_codex_file(path, dry_run=args.dry_run):
                    count += 1
    
    print(f"Total files normalized: {count}")

if __name__ == '__main__':
    main()
