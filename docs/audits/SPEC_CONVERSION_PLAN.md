# Spec Conversion Plan (Phase M)

**Goal**: Reduce `golden.spec` usage from 40 to ≤ 35 (Wave 1), then eventually 0.
**Method**: Use `scripts/capture_golden_via_unified_runner.py` to produce `golden.run.json` (execution) or `golden.state.json` (filesystem).

## Conversion Queue

| Slug | World | Current | Target | Blocker | Owner Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cli-globs-search` | CLI | Spec | State | | [DONE] Converted to State |
| `git-branches` | Git | Spec | State | | [DONE] Convert to State |
| `git-log` | Git | Spec | Run | | [DONE] Captured `git log` output |
| `git-merge-conflict` | Git | Spec | State/Run | | [DONE] Capture outcome |
| `git-rebase-onto-main` | Git | Spec | State | | [DONE] Capture outcome |
| `git-tags` | Git | Spec | Run | | [DONE] Capture `git tag` output |
| `js-arrays-q1-basics` | JS | Spec | Run | | [DONE] Capture node run |
| `js-arrays-q2-map-filter-reduce` | JS | Spec | Run | | [DONE] Capture node run |
| `js-async-q1-promises-basics` | JS | Spec | Run | | [DONE] Capture node run |
| `js-control-q1-if-else-loops` | JS | Spec | Run | | [DONE] Capture node run |
| `js-errors-q1-try-catch` | JS | Spec | Run | | [DONE] Capture node run |
| `js-functions-q1-arrow-vs-regular` | JS | Spec | Run | | [DONE] Capture node run |
| `js-modules-q1-import-export` | JS | Spec | Run | | [DONE] Capture node run |
| `js-objects-q1-properties-methods` | JS | Spec | Run | | [DONE] Capture node run |
| `quest-ts-hello-console` | Quest TS | Spec | Run | | [DONE] Capture node run |
| `quest-ts-hello-variable` | Quest TS | Spec | Run | | [DONE] Capture node run |
| `quest-ts-loop-countdown` | Quest TS | Spec | Run | | [DONE] Capture node run |
| `react-components` | React | Spec | Run | | [DONE] Capture test run |
| `react-conditional-render` | React | Spec | Run | | [DONE] Capture test run |
| `react-context-theme` | React | Spec | Run | | [DONE] Capture test run |
| `react-effects-mount` | React | Spec | Run | | [DONE] Capture test run |
| `react-ignition` | React | Spec | Run | | [DONE] Capture test run |
| `react-lists` | React | Spec | Run | | [DONE] Capture test run |
| `react-props` | React | Spec | Run | | [DONE] Capture test run |
| `react-reducer-cart` | React | Spec | Run | | [DONE] Capture test run |
| `react-state-counter` | React | Spec | Run | | [DONE] Capture test run |
| `react-state-toggle` | React | Spec | Run | | [DONE] Capture test run |
| `ts-arrays` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-control` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-functions` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-generics` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-generics-q2-result-type` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-ignition` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-ignition-q1-types-and-interfaces` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-interfaces` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-modules` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-narrowing-q2-unions-and-guards` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-objects` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-types` | TS | Spec | Run | | [DONE] Capture node run |
| `ts-vars` | TS | Spec | Run | | [DONE] Capture node run |

## Wave 1 Targets (5 Quests)

1. `ts-ignition` (TS) -> Run
2. `ts-vars` (TS) -> Run
3. `react-ignition` (React) -> Run
4. `git-log` (Git) -> Run
5. `cli-globs-search` (CLI) -> State

## Wave 2 Targets (5 Quests)

1. `git-branches` (Git) -> State [DONE]
2. `git-rebase-onto-main` (Git) -> State [DONE]
3. `git-tags` (Git) -> Run [DONE]
4. `git-merge-conflict` (Git) -> State [DONE]
5. `js-arrays-q1-basics` (JS) -> Run [DONE]

## Wave 3 Targets (5 Quests)

1. `js-arrays-q2-map-filter-reduce` (JS) -> Run [DONE]
2. `js-async-q1-promises-basics` (JS) -> Run [DONE]
3. `js-control-q1-if-else-loops` (JS) -> Run [DONE]
4. `js-errors-q1-try-catch` (JS) -> Run [DONE]
5. `js-functions-q1-arrow-vs-regular` (JS) -> Run [DONE]

## Wave 4 Targets (5 Quests)

1. `js-modules-q1-import-export` (JS) -> Run [DONE]
2. `js-objects-q1-properties-methods` (JS) -> Run [DONE]
3. `quest-ts-hello-console` (Quest TS) -> Run [DONE]
4. `quest-ts-hello-variable` (Quest TS) -> Run [DONE]
5. `quest-ts-loop-countdown` (Quest TS) -> Run [DONE]

## Wave 5 Targets (5 Quests)

1. `ts-arrays` (TS) -> Run [DONE]
2. `ts-control` (TS) -> Run [DONE]
3. `ts-functions` (TS) -> Run [DONE]
4. `ts-generics` (TS) -> Run [DONE]
5. `ts-generics-q2-result-type` (TS) -> Run [DONE]

## Wave 6 Targets (5 Quests)

1. `ts-ignition-q1-types-and-interfaces` (TS) -> Run [DONE]
2. `ts-interfaces` (TS) -> Run [DONE]
3. `ts-modules` (TS) -> Run [DONE]
4. `ts-narrowing-q2-unions-and-guards` (TS) -> Run [DONE]
5. `ts-objects` (TS) -> Run [DONE]

## Wave 7 Targets (5 Quests)

1. `ts-types` (TS) -> Run [DONE]
2. `react-components` (React) -> Run [DONE]
3. `react-conditional-render` (React) -> Run [DONE]
4. `react-context-theme` (React) -> Run [DONE]
5. `react-effects-mount` (React) -> Run [DONE]

## Wave 8 Targets (Final)

1. `react-lists` (React) -> Run [DONE]
2. `react-props` (React) -> Run [DONE]
3. `react-reducer-cart` (React) -> Run [DONE]
4. `react-state-counter` (React) -> Run [DONE]
5. `react-state-toggle` (React) -> Run [DONE]
