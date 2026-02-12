# Tutorial — Redirection

## The two operators you’re learning
- `>`  writes to a file (overwrites / creates)
- `>>` appends to a file

## A common pattern
1) Write the first line with `>`
2) Append the body with `>>`
3) Append the final line with `>>`

## Tips
- `cat fixtures/data.txt >> outputs/report.txt` appends the entire file.
- Don’t `echo` the body; read it from the fixture to preserve it exactly.
