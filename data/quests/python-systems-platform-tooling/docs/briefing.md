# Briefing: Internal Tooling & DX

## The Mission
Our engineering team is wasting too much time on manual data cleanup. We need a set of robust, internal utility tools to automate common tasks like generating URL-safe slugs and de-duplicating configuration lists.

Your mission is to build the "Toolbox Core"—a pure logic engine that powers our internal CLI.

## Objectives
- Implement `slugify(text)`:
  - Convert to lowercase and trim.
  - Remove non-alphanumeric characters (except dashes).
  - Collapse spaces and multiple dashes into a single `-`.
  - Strip leading/trailing dashes.
- Implement `unique_sorted(items)`:
  - Trim and lowercase all strings.
  - Remove empty strings.
  - Return a deduplicated list sorted alphabetically.
- Implement the `run_tool_request` dispatcher:
  - Route requests to the correct tool (`slugify`, `sum`, `unique_sorted`).
  - Handle bad inputs gracefully by returning error codes (`EF_TOOL_BAD_INPUT`, `EF_TOOL_UNKNOWN`).

## Constraints
- No external libraries. Use standard `re` for regex operations.
- The output must be a standardized response dictionary.
