# Approvals + Diffs

Implement `apply_diff(base, diff, approved)`.

Diff is a list of edits: {start:int, end:int, text:str}
- start/end are indices into base (end exclusive)
- apply edits in order
- if approved is False: raise PermissionError
