---
title: Approvals and Diffs
id: agents/approvals-and-diffs
---
# Approvals and Diffs

Human-in-the-loop controls for agent actions.

## Approval Gates
- **Before**: Validate plan before execution
- **After**: Review results before application
- **Critical**: Require approval for high-risk changes

## Diff Presentation
```python
diff = compute_diff(current_state, proposed_state)
if requires_approval(diff):
    approved = request_human_approval(diff)
    if not approved:
        raise ApprovalDenied()
```
