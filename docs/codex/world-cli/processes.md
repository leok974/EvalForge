---
id: glossary/cli/processes
title: Processes
world: cli
---

# Processes

A **process** is a running instance of a program.

## Key Concepts

- **PID** (Process ID) — unique number identifying the process
- **Parent/Child** — processes can spawn other processes
- **Foreground** — interactive, blocks your terminal
- **Background** — runs without blocking the terminal

## Viewing Processes

```bash
# List all processes
ps aux          # Unix/Linux/Mac
Get-Process     # PowerShell

# Live updating view
top             # Unix/Linux/Mac  (press 'q' to quit)
htop            # Better alternative (if installed)

# Filter by name
ps aux | grep python
Get-Process -Name python
```

## Managing Processes

### Running in Background

```bash
# Start in background
long_command &

# Move running process to background
# 1. Press Ctrl+Z (suspend)
# 2. Type: bg
```

### Bringing to Foreground

```bash
fg
```

### Killing Processes

```bash
# Graceful termination
kill PID
kill -TERM PID

# Force kill
kill -9 PID
kill -KILL PID

# Kill by name
pkill python
killall python
```

## Common Scenarios

### Find and kill a stuck process

```bash
# 1. Find PID
ps aux | grep myapp

# 2. Kill it
kill 12345
```

### Monitor resource usage

```bash
top
# Press 'M' to sort by memory
# Press 'P' to sort by CPU
```

## Related Concepts

- [Signals](codex:glossary/cli/signals)