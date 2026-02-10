# Infra Ignition: Preflight Checks

Edit task.sh so it:
1) reads fixtures/tools.txt (required tools, one per line)
2) reads fixtures/which.txt (installed tools, one per line)
3) writes outputs/preflight.txt:

STATUS=OK|FAIL
MISSING=tool1,tool2 (empty after '=' if none)

If any missing tools exist:
- print MISSING_TOOLS to stderr
- exit code 10
Otherwise exit 0.
