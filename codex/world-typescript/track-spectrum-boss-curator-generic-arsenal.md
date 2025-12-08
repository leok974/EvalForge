# Codex: Curator of the Generic Arsenal

> *“Why forge a new blade for every battle when you can craft a weapon that fits any warrior?”*

The Curator oversees a vault of generic tools: pluckers, groupers, indexers. Every team has reinvented them in their own way. Your task is to build a single, coherent toolkit.

## Mission

Build a small, generic collection library:

- `pluck<T, K extends keyof T>(items: T[], key: K): T[K][]`
- `groupBy<T, K extends keyof T>(items: T[], key: K): Record<string, T[]>`
- `indexBy<T, K extends keyof T>(items: T[], key: K): Record<T[K] & (string | number | symbol), T>`
- `mergeById<T, K extends keyof T>(existing: T[], incoming: T[], idKey: K): T[]`
- `ensureUnique<T, K extends keyof T>(items: T[], key: K): T[]`

The core virtues:

- **Generic**: Works for any T, not just User or Job.
- **Inference-friendly**: Callers rarely need explicit type arguments.
- **No any** in the public API.
- **Predictable semantics**: No surprising mutations or side effects.

You will also write a small usage example that consumes these helpers in a fake feature module (e.g., jobs list, notifications, or users).

## What the Curator Cares About

- Clean generic signatures that reflect how teams will actually use them.
- Good type inference at call sites (no casting roulette).
- Clear, tested behavior for edge cases (empty arrays, duplicate IDs, etc.).

If your toolkit feels like something you’d extract into a shared package for a real codebase, you pass the Curator’s trial.
