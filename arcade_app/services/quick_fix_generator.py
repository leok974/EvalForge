import re
from typing import List, Optional, Dict, Any
from arcade_app.schemas.quest_run import QuickFix

def generate_quick_fixes(
    language: str,
    failure_summary: Optional[Dict[str, Any]],
    diagnostics: List[Dict[str, Any]],
    objective_results: List[Dict[str, Any]],
    workspace_snapshot: Dict[str, Any],
    hidden_tests_reveal: bool = False
) -> List[QuickFix]:
    """
    Generates a list of Quick Fix actions based on run failure data.
    """
    fixes: List[QuickFix] = []

    # 1. Check for Indentation Errors (Tabs vs Spaces) - High Priority
    #    Target: IndentationError in Python, or generic Mixed Spaces/Tabs check if diagnostic suggests it.
    if language == "python":
        indent_error = next((d for d in diagnostics if 
            "IndentationError" in d.get("message", "") or 
            "TabError" in d.get("message", "") or
            "inconsistent use" in d.get("message", "").lower() or
            "indentation" in d.get("message", "").lower()
        ), None)
        if indent_error:
            path = indent_error.get("path")
            
            # Helper to loose match path if exact match fails
            content_node = workspace_snapshot.get(path)
            if not content_node and path:
                # Try basename match 
                import os
                basename = os.path.basename(path)
                content_node = workspace_snapshot.get(basename)

            # Determine effective file content
            content = content_node.get("content") if content_node else None
             
            
            # Simple heuristic: If content has tabs, suggest converting to spaces
            if content and "\t" in content:
                # Replace all tabs with 4 spaces
                new_content = content.replace("\t", "    ")
                
                # Hardening: Check limits
                # Limit patch size (e.g., 50KB to prevents huge payloads)
                if len(new_content) > 50_000:
                    # Too large to safe-patch automatically
                    pass 
                else:
                    fixes.append(QuickFix(
                        id="fix-tabs-to-spaces",
                        kind="apply_patch",
                        title="Convert tabs to spaces",
                        why="Python requires consistent indentation. Mixed tabs and spaces cause errors.",
                        severity="safe",
                        locator={"path": path, "line": indent_error.get("line"), "column": 1},
                        patch={"path": path, "replacement_full_content": new_content}
                    ))
    
    # 2. Check for Output Mismatch (Stdout Regex)
    #    Trigger: Primary failure is output_mismatch OR specific objective failed
    output_fail = next((res for res in objective_results if res.get("ok") is False and res.get("kind") == "stdout_regex"), None)
    
    if output_fail:
        # User defined label often contains the expected string description, but we want the raw regex or hint if possible.
        # Ideally, the objective definition (which we don't fully have here, just results) would pass a hint.
        # But `objective_results` usually just has id, ok, detail.
        # We'll rely on a generic suggestion or try to parse detail if it says "Expected matches: ..."
        
        # Generic Snippet Construction
        snippet_code = ""
        user_hint = "Print the expected output"
        
        if language == "python":
            snippet_code = 'print("Expected Output")'
        elif language in ["javascript", "typescript"]:
            snippet_code = 'console.log("Expected Output");'
            
        fixes.append(QuickFix(
            id="fix-output-mismatch",
            kind="copy_snippet",
            title="Print expected output",
            why="Your code didn't print what the quest expects. Use this snippet to verify output.",
            severity="suggestion",
            snippet=snippet_code
        ))

    # 3. Hidden Tests Failure (Safe Version)
    primary_failure = (failure_summary or {}).get("primary_failure", {})
    if primary_failure.get("kind") == "hidden_tests_failed":
        # Safe nudge, absolutely no leakage
        fixes.append(QuickFix(
            id="fix-check-edge-cases",
            kind="copy_snippet", # Actually just a text snippet/comment
            title="Edge Case Checklist",
            why="Your code passed public tests but failed hidden ones. Check these common edge cases:",
            severity="suggestion",
            snippet=(
                 "# Checklist:\n"
                 "# [ ] Empty inputs?\n"
                 "# [ ] Negative numbers / Zero?\n"
                 "# [ ] Off-by-one errors?\n"
                 "# [ ] Type mismatch?"
            )
        ))

    # 4. Jump to First Error (Navigate)
    #    Always added if diagnostics exist and we haven't added a specific patch for it yet
    #    (or even if we did, navigation is useful)
    if diagnostics and not any(f.kind == "apply_patch" for f in fixes):
        first_diag = diagnostics[0]
        fixes.append(QuickFix(
            id="nav-first-error",
            kind="navigate",
            title=f"Jump to {first_diag.get('message', 'Error')[:30]}...",
            why="Locate the source of the error.",
            severity="safe",
            locator={"path": first_diag.get("path"), "line": first_diag.get("line"), "column": first_diag.get("column")}
        ))
        
    return fixes[:3] # Cap at 3
