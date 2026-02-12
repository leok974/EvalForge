# Redirection

Edit `task.sh` to generate `outputs/report.txt`.

## Output Contract
`outputs/report.txt` must contain exactly:

1) First line:
```

HEADER

```

2) Then **all lines** from:
`fixtures/data.txt`

3) Last line:
```

FOOTER

```

## Rules
- Preserve the data lines exactly as they appear in `fixtures/data.txt`.
- Use output redirection operators (`>` and `>>`) to build the file.
- No extra stdout/stderr output. Exit code must be 0.
