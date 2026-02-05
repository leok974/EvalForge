---
id: glossary/cli/signals
title: Signals
world: cli
---

# Signals

**Signals** are notifications sent to processes to trigger specific actions (pause, resume, terminate, etc.).

## Common Signals

| Signal | Number | Meaning | Can Ignore? |
|--------|--------|---------|-------------|
| `SIGINT` | 2 | Interrupt (Ctrl+C) | Yes |
| `SIGTERM` | 15 | Graceful termination | Yes |
| `SIGKILL` | 9 | Force kill immediately | **No** |
| `SIGSTOP` | 19 | Pause process | **No** |
| `SIGCONT` | 18 | Resume process | N/A |
| `SIGHUP` | 1 | Hangup (terminal closed) | Yes |

## Sending Signals

```bash
# Send signal to PID
kill -SIGNAL PID

# Examples:
kill -TERM 12345    # Graceful shutdown
kill -KILL 12345    # Force kill
kill -STOP 12345    # Pause

# Keyboard shortcuts
# Ctrl+C  → SIGINT
# Ctrl+Z  → SIGSTOP
```

## Graceful vs Force

### SIGTERM (15) — Graceful
- Process can clean up (close files, save state, etc.)
- **Use this first**

### SIGKILL (9) — Force
- Immediate termination, no cleanup
- Use only when SIGTERM fails
- Can leave corrupt data or orphaned resources

## Handling Signals in Scripts

```bash
#!/bin/bash

cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
    exit 0
}

trap cleanup SIGINT SIGTERM

# Your script logic...
while true; do
    sleep 1
done
```

## Best Practices

- Try SIGTERM before using SIGKILL
- Use `trap` in scripts for cleanup on exit
- Understand that SIGKILL and SIGSTOP **cannot be caught**

## Related Concepts

- [Processes](codex:glossary/cli/processes)