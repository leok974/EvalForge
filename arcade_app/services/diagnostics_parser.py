import re
from typing import List, Dict, Optional
from pydantic import BaseModel

class Diagnostic(BaseModel):
    path: str
    line: int
    column: int = 1
    severity: str = "error" # error, warning
    kind: str = "runtime" # syntax, runtime, test
    message: str

def parse_diagnostics(stderr: str, language: str, workspace_files: List[str]) -> List[Dict]:
    """
    Parses stderr to extract structured diagnostics.
    """
    diagnostics = []
    
    # Normalize workspace files for easier matching (set of relative paths)
    # Assumes workspace_files are like "src/main.py", "tests/test_main.py"
    valid_files = set(workspace_files)
    
    lines = stderr.split('\n')
    
    if language == "python":
        diagnostics.extend(_parse_python_traceback(lines, valid_files))
    else:
        # Generic / JS / TS (Bun)
        diagnostics.extend(_parse_generic_error(lines, valid_files))
        
    # Deduplicate based on path+line+message
    seen = set()
    unique_diagnostics = []
    for d in diagnostics:
        key = (d['path'], d['line'], d['message'])
        if key not in seen:
            seen.add(key)
            unique_diagnostics.append(d)
            
    return unique_diagnostics[:20] # Cap at 20

def _parse_python_traceback(lines: List[str], valid_files: set) -> List[Dict]:
    diags = []
    # Pattern: File "path/to/file.py", line 10, in <module>
    file_pattern = re.compile(r'File "(?P<path>.*?)", line (?P<line>\d+)(?:, in (?P<scope>.*))?')
    
    # SyntaxError pattern often shows:
    #   File "main.py", line 1
    #     print("hello"
    #           ^
    # SyntaxError: '(' was never closed
    
    # We want to capture the LAST frame in the workspace (for runtime errors)
    # OR the specific location of a SyntaxError.
    
    # Iterate lines to find frames
    current_error = None
    frames = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        match = file_pattern.search(line)
        if match:
            path = match.group('path')
            # Sanitize path: remove /workspace/ prefix if present
            clean_path = path.replace("/workspace/", "").replace("\\", "/") # normalize to forward slash
            
            if clean_path in valid_files:
                line_num = int(match.group('line'))
                frames.append({
                    "path": clean_path,
                    "line": line_num,
                    "index": i
                })
        
        # Check for exception type at end (e.g. "NameError: ...")
        # Usually valid python exception lines start with `NameError:` or `ZeroDivisionError:` etc.
        # But ensure it's not part of code snippet
        if not line.startswith('File "') and not line.startswith('^') and ': ' in line:
            # Simple heuristic: CamelCaseError: message
            parts = line.split(': ', 1)
            if 'Error' in parts[0] or 'Exception' in parts[0]:
               current_error = {
                   "kind": "syntax" if "Syntax" in parts[0] or "Indentation" in parts[0] else "runtime",
                   "message": line,
                   "index": i
               }

    # Strategy:
    # 1. If SyntaxError/IndentationError, usually the File line immediately precedes the error line OR the code snippet.
    #    Python tracebacks for syntax are:
    #    File "...", line N
    #      code
    #      ^
    #    SyntaxError: ...
    
    if current_error and current_error['kind'] == 'syntax':
        # Find the frame closest to the error message (scanning backwards from error index)
        # Actually in python < 3.10 stack traces, File line is above, then code, then carret, then error.
        # We need to find the File line that corresponds to this error.
        # Simplification: Use the last frame found before the error message.
        relevant_frame = None
        for frame in reversed(frames):
            if frame['index'] < current_error['index']:
                relevant_frame = frame
                break
        
        if relevant_frame:
            diags.append({
                "path": relevant_frame['path'],
                "line": relevant_frame['line'],
                "column": 1, # TODO: Parse caret line if possible
                "severity": "error",
                "kind": "syntax",
                "message": current_error['message']
            })
            return diags

    # 2. If Runtime Error, find the LAST frame that is within our workspace (Valid Files).
    #    Tracebacks show call stack most recent call last.
    elif current_error: # Runtime error
        # Find deepest frame in workspace
        relevant_frame = None
        if frames:
            relevant_frame = frames[-1] # Last one
        
        if relevant_frame:
            diags.append({
                "path": relevant_frame['path'],
                "line": relevant_frame['line'],
                "column": 1,
                "severity": "error",
                "kind": "runtime",
                "message": current_error['message']
            })
            return diags
            
    # Fallback to collecting all frames if no clear error message bottom line found? 
    # Or just return nothing if we can't parse an error type.
    
    return diags

def _parse_generic_error(lines: List[str], valid_files: set) -> List[Dict]:
    diags = []
    # Unix-style pattern: src/main.ts:10:5: error: message
    # Or: /workspace/src/main.ts:10:5
    
    # Pattern: (path):(line):(col?):? (message)
    pattern = re.compile(r'(?P<path>[a-zA-Z0-9_\-./\\]+\.(ts|js|jsx|tsx|py)):(?P<line>\d+)(:(?P<col>\d+))?')
    
    for line in lines:
        line = line.strip()
        match = pattern.search(line)
        if match:
            path = match.group('path')
            # Cleanup
            clean_path = path.replace("/workspace/", "").replace("\\", "/")
            
            if clean_path in valid_files:
                line_num = int(match.group('line'))
                col_num = int(match.group('col')) if match.group('col') else 1
                
                # Extract message: everything after the match
                # The match usually is "src/main.ts:10:5"
                # The message might follow ": "
                
                # Find where the match ends in the line
                match_end = match.end()
                remainder = line[match_end:].strip()
                if remainder.startswith(':'):
                    remainder = remainder[1:].strip()
                
                message = remainder if remainder else "Error"
                
                diags.append({
                    "path": clean_path,
                    "line": line_num,
                    "column": col_num,
                    "severity": "error",
                    "kind": "runtime", # Default to runtime/generic
                    "message": message
                })
    return diags
