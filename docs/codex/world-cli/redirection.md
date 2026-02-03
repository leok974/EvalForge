# Redirection

**Redirection** controls where command output goes and where input comes from.

## Output Redirection

| Syntax | Meaning |
|--------|---------|
| `>` | Overwrite file with stdout |
| `>>` | Append stdout to file |
| `2>` | Redirect stderr (errors) |
| `&>` | Redirect both stdout and stderr |

## Examples

```bash
# Save output to file (overwrites)
ls > files.txt

# Append to file
echo "new line" >> log.txt

# Discard errors
command 2> /dev/null

# Save everything (output + errors)
script.sh &> output.log
```

## Input Redirection

```bash
# Read from file instead of keyboard
sort < unsorted.txt

# Here document (multi-line input)
cat << EOF
Line 1
Line 2
EOF
```

## Common Mistakes

- Using `>` when you meant `>>` (data loss!)
- Forgetting to redirect stderr separately
- Redirecting to the same file you're reading from

## Related Concepts

- [Pipes](codex:glossary/cli/pipes)
