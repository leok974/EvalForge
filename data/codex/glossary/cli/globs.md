# Globs

**Globs** (or wildcards) are pattern-matching shortcuts for selecting multiple files at once.

## Common Patterns

| Pattern | Matches |
|---------|---------|
| `*` | Any number of characters (except `/`) |
| `?` | Exactly one character |
| `[abc]` | One character from the set |
| `[a-z]` | One character in the range |
| `{foo,bar}` | Either "foo" or "bar" (brace expansion) |

## Examples

```bash
# All .txt files in current directory
ls *.txt

# All files starting with "test"
rm test*

# Files like report1.pdf, report2.pdf
ls report?.pdf

# All .js and .ts files
ls *.{js,ts}
```

## Important Notes

- Globs are **expanded by the shell** before the command runs
- `*` does **not** match hidden files (those starting with `.`)
- Use quotes to prevent expansion: `ls '*.txt'`

## Related Concepts

- [Search](codex:glossary/cli/search)
