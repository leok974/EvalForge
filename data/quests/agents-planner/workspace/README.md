# Planner

Implement `plan(request, tool_names)`.

Supported request forms:
- "add <a> <b>" -> tool "add" args {a:int,b:int}
- "echo <text...>" -> tool "echo" args {text:str}
Raises ValueError("NO_TOOL") if required tool missing.
