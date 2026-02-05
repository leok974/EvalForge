---
id: glossary/cli/scripting-basics
title: Scripting Basics
world: cli
---

# Scripting Basics

**Shell scripts** automate command sequences and add logic (conditions, loops, etc.).

## Creating a Script

1. Create a file (e.g., `backup.sh`)
2. Add shebang line at the top
3. Write your commands
4. Make executable

```bash
#!/bin/bash

echo "Starting backup..."
tar -czf backup.tar.gz ~/documents
echo "Backup complete!"
```

```bash
chmod +x backup.sh
./backup.sh
```

## Shebang (`#!`)

Tells the OS which interpreter to use.

```bash
#!/bin/bash          # Bash
#!/usr/bin/env python3  # Python
#!/usr/bin/env node     # Node.js
```

## Arguments

Access command-line arguments with `$1`, `$2`, etc.

```bash
#!/bin/bash

echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
```

```bash
./script.sh hello world
# First argument: hello
# Second argument: world
```

## Variables

```bash
#!/bin/bash

NAME="Alice"
COUNT=5

echo "Hello, $NAME"
echo "Count: $COUNT"

# Command substitution
FILES=$(ls | wc -l)
echo "Files in directory: $FILES"
```

## Conditions

```bash
#!/bin/bash

if [ -f "config.txt" ]; then
    echo "Config found"
else
    echo "Config missing"
    exit 1
fi
```

## Loops

```bash
#!/bin/bash

# For loop
for file in *.txt; do
    echo "Processing $file"
done

# While loop
COUNT=0
while [ $COUNT -lt 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done
```

## Safe Defaults

```bash
#!/bin/bash

# Exit on error
set -e

# Exit on undefined variable
set -u

# Fail on pipe errors
set -o pipefail

# Combined:
set -euo pipefail
```

## Best Practices

- Use `set -euo pipefail` for safety
- Quote variables: `"$VAR"` (prevents word splitting)
- Check arguments exist before using
- Provide usage/help messages
- Use meaningful exit codes

## Related Concepts

- [Exit Codes](codex:glossary/cli/exit-codes)
- [Environment Variables](codex:glossary/cli/env-vars)