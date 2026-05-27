# World-Python Pedagogical Audit
## Date: 2026-05-27
## Auditor: Agent (Sprint 25)

---

## Executive Summary

**Quests audited:** 20  
**CRITICAL findings:** 4  
**IMPORTANT findings:** 7  
**POLISH findings:** 5  
**Clean:** 4  

World-python has two distinct problems. First, **stale documentation**: several quests have tutorials, hints, and examples written for an older version of the quest while the stub (`main.py`/`task.py`) and grading tests were updated without corresponding doc updates. Four quests fall into this category and are rated CRITICAL because the learner, reading the provided docs, will build the wrong program entirely. Second, **hidden test requirements**: six quests test behaviours never mentioned in any learner-facing file — extra required output keys, specific sentinel strings, or validation guards that appear only in the test suite. A learner following all provided docs will produce code that passes every documented requirement and still fail the grader.

The Selenium track (`python-selenium`, 5 quests) is the best-maintained track: internally consistent, well-paced, and fully solvable from the provided materials. The `python-ignition` tier-2 quests are mostly coherent but suffer from hidden requirements. The `python-systems` track has the stale-documentation problem concentrated in three quests. The `python-foundry` track has one coherent quest pair (`hello-variable`, `first-sparks`) and one CRITICAL mismatch (`python-loop` briefing vs. test).

---

## Per-Quest Findings

---

### `first-sparks` · python-foundry · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | Briefing, tutorial, example, stub, test all converge on one task |
| Q2 Sufficiency | SUFFICIENT | Tutorial is self-contained; f-strings in hint 2 not taught but not blocking |
| Q3 Calibration | ON_TARGET | First-quest simplicity: one loop, one post-loop print |
| Q4 Hint Progression | WELL_STAGED | concept → format → placement; hint 2 gives away loop body but acceptable for quest 1 |
| Q5 Concept Coverage | DIRECT | Tutorial teaches `range(3,0,-1)`, loop body, and post-loop statement |
| Q6 Solvability | SOLVED_FROM_DOCS | Cold reader can write the correct program from tutorial alone |

**Findings (POLISH):**
- Hint 2 introduces f-strings (`f"T-minus {i}"`) but the tutorial only shows `print()` with literal strings. A learner who doesn't know f-strings might use concatenation (`"T-minus " + str(i)`) and still pass — but the hint implies f-strings are the expected approach without explaining them. Consider adding one sentence on f-strings to the tutorial or changing hint 2 to show both approaches.

---

### `hello-variable` · python-foundry · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | All artefacts describe the same two-line program |
| Q2 Sufficiency | SUFFICIENT | Briefing specifies exact variable name and value |
| Q3 Calibration | ON_TARGET | Ideal first-concept quest |
| Q4 Hint Progression | WELL_STAGED | Hints provide precision (casing), not code |
| Q5 Concept Coverage | DIRECT | Tutorial directly teaches assignment and `print(variable)` |
| Q6 Solvability | SOLVED_FROM_DOCS | |

**Findings:** None. This is the reference example of a well-designed foundry quest.

---

### `python-loop` · python-foundry · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MAJOR_DRIFT | Briefing and tutorial describe a print-based loop; stub and test check a list-returning function |
| Q2 Sufficiency | INSUFFICIENT | Tutorial models print-based output; stub demands `generate_evens(limit) -> list[int]` |
| Q3 Calibration | ON_TARGET | Function-return version is right for foundry; contradictions obscure this |
| Q4 Hint Progression | GIVES_AWAY_SOLUTION | Hint 3 pastes the complete print-based implementation — which is the wrong architecture for the test |
| Q5 Concept Coverage | UNRELATED | Tutorial teaches filtering + counter pattern (print-based); test checks return value |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Cold reader following briefing+tutorial will produce a print-based program that fails the test entirely |

**Findings (CRITICAL):**  
The briefing says "iterate 1–10, print even numbers, then print `EVEN_COUNT=<total>`". The tutorial models this print-based approach. The stub (`main.py`) asks for `generate_evens(limit: int) -> list[int]` returning a list. The test imports `generate_evens` and checks return values — `EVEN_COUNT` never appears in the test. Hint 3 pastes a complete print-based solution that **will not pass the test**. A learner following every provided doc will write the wrong program.

**Proposed fix (Sprint 26):**  
Rewrite `docs/briefing.md` and `docs/tutorial.md` to describe the function-return contract (`generate_evens(limit)` returning a list of even numbers). Replace hint 3 with a staged hint about list accumulation, not a full solution. The stub and test are correct; the docs are the problem.

---

### `python-data-forge` · python-boss · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MAJOR_DRIFT | Briefing/tutorial/hints=JSON normalization pipeline; stub+test=CSV sales aggregation |
| Q2 Sufficiency | INSUFFICIENT | Tutorial teaches JSON; test requires `csv.DictReader`, float arithmetic, dict accumulation |
| Q3 Calibration | ON_TARGET | CSV sales task is appropriate boss-level; but doc mismatch makes it appear harder |
| Q4 Hint Progression | FLAT | All three hints describe the wrong task (JSON sorting, `json.dumps`) |
| Q5 Concept Coverage | UNRELATED | Tutorial covers `itemgetter` and JSON coercion; test checks CSV aggregation |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | A learner reading the briefing will implement a JSON normalizer; the test checks CSV functions |

**Findings (CRITICAL):**  
The briefing describes reading `fixtures/raw_contacts.json`, normalizing records, and printing sorted JSON. The tutorial teaches type coercion and `json.dumps`. The example shows `normalize_record()` and JSON output. But `main.py` asks for `load_sales(path)`, `revenue_by_item(rows)`, `top_items(revenue, k)` against a CSV. The test checks CSV loading, float arithmetic, and top-k ordering. None of the in-quest docs mention CSV, `csv.DictReader`, or the `sales.csv` fixture. This is a complete narrative swap — two entirely different quests are inhabiting one shell.

**Proposed fix (Sprint 26):**  
Rewrite `docs/briefing.md`, `docs/tutorial.md`, `docs/hints.md`, and `workspace/example.py` to describe the CSV sales pipeline. Tutorial should cover `csv.DictReader`, string-to-float casting, and dict accumulation. Alternatively, replace `main.py` and the grading tests with a JSON normalization implementation to match the existing documentation — but the CSV version is the better boss-level task.

---

### `python-systems-service-boundaries` · python-systems · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MINOR_DRIFT | Briefing, stub, and tests agree on `close_ticket`/`InMemoryTicketRepo`; tutorial uses wrong mutation pattern |
| Q2 Sufficiency | NEEDS_OUTSIDE_KNOWLEDGE | `dataclasses.replace()` is not in tutorial or hints; only in `example.py` |
| Q3 Calibration | ON_TARGET | Repository pattern + service boundary is appropriate for python-systems |
| Q4 Hint Progression | WELL_STAGED | Hints stage dict operations, then KeyError handling, then save reminder — no mention of frozen issue |
| Q5 Concept Coverage | ADJACENT | Tutorial covers service boundaries correctly but demonstrates mutable mutation for a frozen dataclass |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Learner who follows tutorial gets `FrozenInstanceError`; must read `example.py` to find `dataclasses.replace()` |

**Findings (IMPORTANT):**  
`docs/tutorial.md` explicitly shows `ticket.status = "closed"` as the update pattern. But `Ticket` is declared `@dataclass(frozen=True)` in the stub — direct attribute assignment will raise `FrozenInstanceError`. The example (`example.py`) correctly uses `dataclasses.replace(user, active=False)` but the tutorial and all three hints are silent on this. A learner reading the tutorial will write semantically correct logic that crashes at runtime.

**Proposed fix (Sprint 26):**  
In `docs/tutorial.md`, replace the mutable-mutation example with a `dataclasses.replace()` example. Add a short callout: "Because `Ticket` is frozen, you cannot set `ticket.status = 'closed'` directly — use `dataclasses.replace(ticket, status='closed')` to create a new instance." Add this to hint 2 or 3 as well.

---

### `python-systems-resilient-job-runner` · python-systems · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | Briefing, tutorial, example, stub, and tests all describe the same function |
| Q2 Sufficiency | SUFFICIENT | Tutorial covers backoff formula, exception chaining, and DI pattern |
| Q3 Calibration | ON_TARGET | Retry with backoff is a real-world systems concept at the right level |
| Q4 Hint Progression | GIVES_AWAY_SOLUTION | Hint 3 pastes the complete working implementation verbatim |
| Q5 Concept Coverage | DIRECT | Tutorial directly teaches every concept the test exercises |
| Q6 Solvability | SOLVED_FROM_DOCS | Tutorial + stub TODOs are sufficient; hint 3 not needed |

**Findings (POLISH):**  
Everything works, but hint 3 pastes the complete solution. This is the best-designed systems quest otherwise — tutorial is excellent, stub TODOs are clear, tests are thorough and test the right things (including `RetryError.__cause__` chaining). Remove the verbatim solution from hint 3; replace with a staged hint about the loop index variable and `raise X from y` syntax.

---

### `python-systems-observability-sli` · python-systems · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MAJOR_DRIFT | Tutorial and briefing are correct; hints are from a different quest; example uses wrong field name |
| Q2 Sufficiency | SUFFICIENT | Tutorial alone is sufficient; hints and example actively mislead |
| Q3 Calibration | ON_TARGET | Simple availability metric is appropriate for python-systems |
| Q4 Hint Progression | FLAT | All three hints belong to the performance-profiling quest (P95 latency, `count_hits`, strategy tie-breaking) |
| Q5 Concept Coverage | DIRECT | Tutorial directly covers the tested skill (`status_code` range check, ratio, rounding) |
| Q6 Solvability | SOLVED_FROM_DOCS | Solvable from tutorial alone; hints would derail a learner |

**Findings (IMPORTANT):**  
All three hints (`docs/hints.md`) describe functions and concepts from the performance-profile quest — they mention `math.ceil`, `P95 latency`, `count_hits`, and strategy tie-breaking. None of these apply to `calculate_availability`. Additionally, `example.py` demonstrates `compute_sli_report()` which uses `event["status"]` (not `event["status_code"]`), creating a field-name trap for any learner who copies the example pattern.

**Proposed fix (Sprint 26):**  
Replace `docs/hints.md` with three staged hints for `calculate_availability`: (1) iterate events with a `sum(1 for e in events if ...)` guard, (2) the range condition `200 <= e["status_code"] <= 399`, (3) `round(successes / total, 4)`. Update `example.py` to use `event["status_code"]` consistently, or add a comment noting the field name difference.

---

### `python-systems-performance-profile` · python-systems · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MAJOR_DRIFT | Tutorial and hints describe a set-vs-list cost comparison; stub and test check token frequency |
| Q2 Sufficiency | INSUFFICIENT | Tutorial doesn't teach `Counter`, regex `findall`, or sort keys |
| Q3 Calibration | ON_TARGET | `most_common_tokens` is appropriate applied-systems work |
| Q4 Hint Progression | FLAT | All three hints reference non-existent functions (`naive_comparisons`, `count_hits`, `choose_strategy`) |
| Q5 Concept Coverage | UNRELATED | Tutorial covers Big O and set membership; tested skill is Counter + sorted |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Solvable from `example.py` + stub alone, but tutorial and hints actively mislead |

**Findings (IMPORTANT):**  
`docs/tutorial.md` describes a deterministic cost model for naive vs. set-based membership checks. `docs/hints.md` references `naive_comparisons`, `count_hits`, and a strategy tie-breaker — functions that don't exist in the stub. The actual task is `most_common_tokens(text, k)` using `Counter` and `sorted`. The tutorial/hints are from an earlier version of this quest that was never replaced when the task was rewritten. `example.py` is correct (shows `word_frequencies` and `top_n` with the right sort key) but is the only accurate doc.

**Proposed fix (Sprint 26):**  
Rewrite `docs/tutorial.md` to cover: regex `findall`, `Counter` from `collections`, `sorted(items, key=lambda kv: (-kv[1], kv[0]))`. Replace `docs/hints.md` with three staged hints: (1) use `_TOKEN_RE.findall(text)` to extract tokens, (2) use `Counter(tokens)` to count, (3) `sorted(..., key=lambda kv: (-kv[1], kv[0]))[:k]` for ordering.

---

### `python-systems-platform-tooling` · python-systems · tier 1

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MAJOR_DRIFT | Briefing/tutorial/hints/example describe `slugify`/`unique_sorted`/`run_tool_request`; stub and test check `parse_semver` |
| Q2 Sufficiency | INSUFFICIENT | No doc mentions semver, `str.split(".")`, `int()` conversion, or `ValueError` for bad format |
| Q3 Calibration | ON_TARGET | `parse_semver` is a reasonable systems-tier task; but no docs support it |
| Q4 Hint Progression | FLAT | All hints describe regex and set operations for the wrong functions |
| Q5 Concept Coverage | UNRELATED | Tutorial covers `re.sub` and dispatcher; tested function is semver string parsing |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Completely unsolvable from provided docs — a different program is documented |

**Findings (CRITICAL):**  
The briefing, tutorial, all three hints, and `example.py` all describe implementing `slugify(text)`, `unique_sorted(items)`, and `run_tool_request(req)`. But `main.py` stub is:

```python
def parse_semver(v): return (0, 0, 0)
```

And the test checks `parse_semver("1.2.3") == (1, 2, 3)`, `ValueError` on `"1.2"`, `ValueError` on `"a.b.c"`. The entire documentation layer is for a different quest. A learner has no way to know what `parse_semver` should do beyond guessing from the function name and the stub's (trivial) return value.

**Proposed fix (Sprint 26):**  
Two options: (A) Replace `main.py` stub and grading tests with the `slugify`/`unique_sorted`/`run_tool_request` task that the docs describe; (B) replace `docs/briefing.md`, `docs/tutorial.md`, `docs/hints.md`, and `example.py` with content for `parse_semver`. Option A is preferable — the documented task is richer and more instructive as a systems quest. Update grading test to check `slugify`, `unique_sorted`, and `run_tool_request` instead of `parse_semver`.

---

### `python-functions-contracts` · python-ignition · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MINOR_DRIFT | Briefing/tutorial describe the validation contract; test requires two undocumented fields/guards |
| Q2 Sufficiency | NEEDS_OUTSIDE_KNOWLEDGE | `"active": True` output field and negative-age guard are not in any learner-facing doc |
| Q3 Calibration | ON_TARGET | Type validation with `isinstance` is right for ignition |
| Q4 Hint Progression | GIVES_AWAY_SOLUTION | Hint 3 pastes the complete implementation (but still missing `"active"` and negative-age) |
| Q5 Concept Coverage | ADJACENT | Tutorial covers type-checking; test also checks output shape and negative-integer rejection |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Learner will fail on `result["active"]` assertion and `age == -5` case |

**Findings (IMPORTANT):**  
Test `test_valid_user` asserts `result["active"] is True` — the `"active"` key must be present in the returned dict. Neither the briefing, tutorial, hints, nor example mention this field. Test `test_invalid_age` includes `age == -5` as an invalid input (negative integer) — the briefing only says "age must be an integer," not "age must be non-negative." Hint 3 pastes a solution that produces the wrong output (missing `"active"`, no negative-age guard).

**Proposed fix (Sprint 26):**  
Add `"active": True` to the briefing's output spec and the tutorial's return value example. Add a note to the briefing that age must be a non-negative integer. Update hint 3 to include both fields.

---

### `python-file-io-safe` · python-ignition · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | Briefing, tutorial, example, and test all describe the same function |
| Q2 Sufficiency | SUFFICIENT | All concepts taught; `from pathlib import Path` is the only missing import in stub |
| Q3 Calibration | ON_TARGET | File I/O with error handling is a practical tier-2 skill |
| Q4 Hint Progression | WELL_STAGED | Concept → skip-invalid-lines → split-limit trick; no giveaway |
| Q5 Concept Coverage | DIRECT | Tutorial covers `pathlib`, `try/except FileNotFoundError`, `split("=", 1)`, `strip()` |
| Q6 Solvability | SOLVED_FROM_DOCS | Example is a reference solution, but tutorial is sufficient independently |

**Findings (POLISH):**  
`task.py` stub does not include `from pathlib import Path`. Beginners at tier 2 may not know to add it. Tutorial shows the import but the stub should include it as a starting scaffold to avoid a confusing `NameError`. Also, `example.py` is a verbatim reference solution — fine pedagogically, but the line between "pattern demonstration" and "copy-paste temptation" is blurry here.

---

### `python-dicts-lists-transform` · python-ignition · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | All artefacts describe `transform_inventory` with the same contract |
| Q2 Sufficiency | SUFFICIENT | Tutorial teaches set comprehension + sum comprehension |
| Q3 Calibration | ON_TARGET | Dict comprehensions are the right ignition-level skill |
| Q4 Hint Progression | GIVES_AWAY_SOLUTION | Hint 3 pastes the complete solution |
| Q5 Concept Coverage | DIRECT | Tutorial directly covers set/sum comprehensions used in the solution |
| Q6 Solvability | SOLVED_FROM_DOCS | Example is the solution; quest is trivially solvable by reading it |

**Findings (POLISH):**  
Example and hint 3 both give away the solution. The educational value of this quest depends entirely on learner discipline (not looking at example before trying). Consider replacing `example.py` with a different aggregation problem (e.g., summing `price` by `color`) to preserve the pedagogical gap.

---

### `python-cli-args` · python-ignition · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MINOR_DRIFT | Briefing describes CLI interface; test checks specific output strings not mentioned anywhere |
| Q2 Sufficiency | NEEDS_OUTSIDE_KNOWLEDGE | "Hello World" output and "Processing N/N..." format are undocumented |
| Q3 Calibration | ON_TARGET | `argparse` is a well-chosen ignition-level skill |
| Q4 Hint Progression | WELL_STAGED | Hints cover mechanics (import, action types, help auto-behavior) without giveaway |
| Q5 Concept Coverage | ADJACENT | Tutorial teaches argparse API well; doesn't teach what the program should print |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Cold reader will build valid argparse program that fails "prints Hello World" test |

**Findings (IMPORTANT):**  
The test expects: default run prints `"Hello World"` once; `--count 3` prints it three times; `--verbose --count 1` prints `"Processing 1/1..."`. None of these strings appear in the briefing, tutorial, or hints. The example shows them, but the briefing should spec them explicitly.

**Proposed fix (Sprint 26):**  
Update `docs/briefing.md` to specify: when run, print `"Hello World"` once per count; with `--verbose`, also print `"Processing {i}/{count}..."` before each "Hello World". The learner should not need to read `example.py` to discover the output contract.

---

### `python-oop-mini` · python-ignition · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MINOR_DRIFT | Briefing documents overdraft protection; test also requires negative-amount guards |
| Q2 Sufficiency | NEEDS_OUTSIDE_KNOWLEDGE | `deposit(-10)` raising `ValueError` is not documented anywhere |
| Q3 Calibration | ON_TARGET | OOP fundamentals with validation logic is right for tier 2 |
| Q4 Hint Progression | WELL_STAGED | Hints address overdraft but not negative amounts |
| Q5 Concept Coverage | ADJACENT | Tutorial covers `__init__` and state; misses exception-raising requirements |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Learner produces working overdraft protection but fails negative-amount tests |

**Findings (IMPORTANT):**  
Test requires `ValueError` for `deposit(-10)` and `withdraw(-10)`. Briefing says only "ensure withdrawals do not exceed current balance" — says nothing about negative amounts in either direction. Tutorial shows `self.balance += amount` with no validation. A learner following docs will correctly protect against overdrafts but will allow negative deposits and withdrawals.

**Proposed fix (Sprint 26):**  
Add to `docs/briefing.md`: "Both `deposit` and `withdraw` must raise `ValueError` if the amount is zero or negative." Add hint 3 (currently "method names must match") as a fourth hint, and use hint 3 for the negative-amount guard.

---

### `python-boss-csv-report` · python-ignition · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MAJOR_DRIFT | Tutorial/example teach CSV-to-CSV aggregation; test expects plain-text report with specific sentinel strings |
| Q2 Sufficiency | INSUFFICIENT | Output format, sentinel strings, and column schema all undocumented |
| Q3 Calibration | ON_TARGET | CSV processing + report generation is appropriate boss-level for ignition |
| Q4 Hint Progression | FLAT | Hint 3 says "fieldnames must match expected headers" — but test expects plain text, not CSV headers |
| Q5 Concept Coverage | UNRELATED | Tutorial teaches `csv.DictWriter`; test expects plain text with `key=value` lines |
| Q6 Solvability | NEEDED_OUTSIDE_KNOWLEDGE | Unsolvable from docs — output format, column names, and sentinels are hidden |

**Findings (CRITICAL):**  
This quest's actual test contract is entirely undisclosed in learner-facing docs:
- Input CSV has columns `id,sales` (example shows `category,amount`)
- Output file must be **plain text** with `TOTAL_SALES=600.00`, `AVG_SALES=200.00`, `COUNT=3` (example uses `csv.DictWriter` with headers)
- Missing input must print `"INPUT_MISSING"` to stdout (not documented)
- Successful run must print `"REPORT_GENERATED"` to stdout (not documented)
- Hint 3 tells the learner to match `fieldnames` — irrelevant for plain text output

A learner will produce a CSV output file (following the tutorial) and print nothing, failing every test assertion.

**Proposed fix (Sprint 26):**  
Rewrite `docs/briefing.md` to specify: input CSV schema (`id`, `sales` columns); output file format (plain text, `TOTAL_SALES=`, `AVG_SALES=`, `COUNT=` lines); required stdout sentinels (`REPORT_GENERATED` on success, `INPUT_MISSING` on missing file). Update `example.py` to use the `id`/`sales` schema and plain-text output format. Update `docs/tutorial.md` to show plain-text file writing alongside CSV reading.

---

### `selenium-open-page` · python-selenium · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MINOR_DRIFT | Hint 3 contradicts briefing on the expected page title |
| Q2 Sufficiency | SUFFICIENT | Tutorial and stub together cover WebDriver setup and title assertion |
| Q3 Calibration | ON_TARGET | First Selenium quest; single concept (navigation + title) |
| Q4 Hint Progression | FLAT | Hint 3 states incorrect title (`"Mock CMS"` vs briefing's `"CMS Login"`) |
| Q5 Concept Coverage | DIRECT | Tutorial covers `driver.get()`, `driver.title`, and assertion |
| Q6 Solvability | SOLVED_FROM_DOCS | Solvable from briefing + tutorial; hint 3 would cause assertion failure if followed |

**Findings (IMPORTANT):**  
`docs/hints.md` hint 3 states: "the mock CMS page title is exactly `'Mock CMS'`." The briefing states the title should be `"CMS Login"`. These are contradictory. A learner who reads hint 3 will write `assert driver.title == "Mock CMS"` which will fail against the actual CMS. The structural test (which only checks that `"TITLE_MATCH"` appears in the code) will still pass, but live browser execution will fail.

**Proposed fix (Sprint 26):**  
Correct hint 3 in `docs/hints.md` to say `"CMS Login"`, matching the briefing.

---

### `selenium-find-elements` · python-selenium · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | MINOR_DRIFT | Briefing says 2 elements; stub and test require 3 |
| Q2 Sufficiency | SUFFICIENT | Exact `data-testid` values provided in stub comments |
| Q3 Calibration | ON_TARGET | CSS selector strategy is appropriate progression |
| Q4 Hint Progression | WELL_STAGED | Minimal, non-giveaway hints |
| Q5 Concept Coverage | DIRECT | Tutorial teaches `By.CSS_SELECTOR` and `data-testid` |
| Q6 Solvability | SOLVED_FROM_DOCS | Stub comments give exact selectors; solvable from stub alone |

**Findings (POLISH):**  
Briefing mentions username and password fields but not the submit button. The stub comments show all three (`login-username`, `login-password`, `login-submit`), and the test checks for all three in the source code. This is a minor inconsistency — update the briefing to mention all three elements.

---

### `selenium-click-and-type` · python-selenium · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | All artefacts describe the same login automation flow |
| Q2 Sufficiency | SUFFICIENT | Tutorial covers `send_keys`, `click`, `WebDriverWait`, PRG pattern |
| Q3 Calibration | ON_TARGET | Good progression from element finding to interaction |
| Q4 Hint Progression | WELL_STAGED | Minimal, non-prescriptive |
| Q5 Concept Coverage | DIRECT | Tutorial directly teaches every required interaction pattern |
| Q6 Solvability | SOLVED_FROM_DOCS | |

**Findings:** None. Well-structured progression quest with appropriate hints.

---

### `selenium-read-text-and-assert` · python-selenium · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | All artefacts describe the same flow (login + read dashboard title) |
| Q2 Sufficiency | SUFFICIENT | Tutorial and example together cover `EC.presence_of_element_located` and `.text` |
| Q3 Calibration | ON_TARGET | Adds explicit waits and text extraction on top of prior skills |
| Q4 Hint Progression | WELL_STAGED | Hints stage concept → wait pattern → assertion form |
| Q5 Concept Coverage | DIRECT | Tutorial directly teaches the wait+read pattern |
| Q6 Solvability | SOLVED_FROM_DOCS | |

**Findings:** None. This is the strongest quest in the Selenium track.

---

### `selenium-take-screenshot` · python-selenium · tier 2

| Q | Score | Notes |
|---|---|---|
| Q1 Coherence | COHERENT | All artefacts describe the same screenshot flow |
| Q2 Sufficiency | SUFFICIENT | Tutorial explains the EvalForge-specific `EVALFORGE_ARTIFACT_DIR` pattern |
| Q3 Calibration | ON_TARGET | Good final Selenium quest; introduces artifact management |
| Q4 Hint Progression | WELL_STAGED | Hint 1 → Hint 2 → Hint 3 stage the path construction progressively |
| Q5 Concept Coverage | DIRECT | Tutorial covers env var, path construction, and screenshot call |
| Q6 Solvability | SOLVED_FROM_DOCS | |

**Findings:** None. Solid final Selenium quest.

---

## Patterns

### Pattern 1: Tutorial/Hint content describes a different quest (5 quests)

**Quests:** `python-data-forge`, `python-systems-performance-profile`, `python-systems-platform-tooling`, `python-systems-observability-sli` (hints only), `python-boss-csv-report`

The most severe recurring failure. Documentation was written for one version of a quest, then the stub and tests were updated to a different task without replacing the docs. In `python-systems-performance-profile` and `python-systems-observability-sli` this is confirmed by all three hints referencing function names (`naive_comparisons`, `count_hits`, `P95 latency`) that appear nowhere in the actual stub. In `python-systems-platform-tooling` the mismatch is three-way: docs describe `slugify`, stub asks for `parse_semver`, and the test checks `parse_semver`.

**Root cause:** The Sprint 24 stub/test rewrites were not accompanied by doc rewrites. The `docs/` folder was not part of the mechanical coherence audit scope.

**Fix pattern:** For each affected quest, the doc layer must be rewritten to match the stub/test layer. The stub and tests are the authority on what the quest actually tests.

---

### Pattern 2: "Full Solution" as hint 3 (5 quests)

**Quests:** `python-loop`, `python-systems-resilient-job-runner`, `python-functions-contracts`, `python-dicts-lists-transform`, and `python-systems-platform-tooling` (indirectly via example)

In five quests, the third hint pastes the complete working implementation. In `python-loop` the pasted solution is for the wrong architecture (print-based instead of return-based), so it is both a giveaway AND incorrect. In `python-functions-contracts` it is correct but missing two requirements (`"active"` field, negative-age guard). In `python-systems-resilient-job-runner` it is correct and gives away an otherwise well-designed quest.

**Intended fix pattern:** The third hint should be the most specific staged hint, not the solution. Reserve full solutions for the `grading/solutions/` directory. Replace hint 3 with a concrete pointer to the specific step or syntax the learner is likely to get wrong.

---

### Pattern 3: Hidden test requirements (5 quests)

**Quests:** `python-functions-contracts`, `python-oop-mini`, `python-boss-csv-report`, `python-cli-args`, `python-loop`

Tests check behaviours that are not mentioned in any learner-facing document:
- `python-functions-contracts`: `"active": True` in output dict, rejection of negative age
- `python-oop-mini`: `ValueError` for negative deposits and withdrawals
- `python-boss-csv-report`: output format, `REPORT_GENERATED`/`INPUT_MISSING` sentinels
- `python-cli-args`: `"Hello World"` and `"Processing N/N..."` output strings
- `python-loop`: return-value contract (briefing describes print-based output)

**Fix pattern:** Every behaviour checked by a grading test must be explicitly specified in `docs/briefing.md`. The briefing is the contract. If the test checks it, the briefing must say it.

---

### Pattern 4: `example.py` is the solution (7 quests)

**Quests:** `python-file-io-safe`, `python-dicts-lists-transform`, `python-cli-args`, `python-boss-csv-report`, and all five Selenium quests

In these quests, `example.py` is a working reference implementation of the task (often nearly identical to what the grading solution would be). This conflates two different purposes: "show a related pattern to learn from" (how `first-sparks` and `hello-variable` use `example.py`) and "show the solution so the learner can look it up" (how these quests use it).

For Selenium quests this is arguably appropriate — the WebDriver setup boilerplate is non-trivial and showing it in full is helpful. For Python function quests, `example.py` being the solution removes the intellectual challenge entirely and creates a copy-paste shortcut.

**Fix pattern:** For non-Selenium quests where `example.py` is the solution, either (a) change `example.py` to demonstrate the same concept on a different problem (as `first-sparks` does), or (b) add a comment block explaining that this is a reference solution available after the learner has attempted the task.

---

### Pattern 5: `tutorial.md` teaches the concept but doesn't anchor to the task interface (4 quests)

**Quests:** `python-loop`, `python-cli-args`, `python-systems-service-boundaries`, `python-boss-csv-report`

In these quests, the tutorial teaches the relevant concept (loops, argparse, repository pattern, CSV reading) in the abstract, but does not show or reference the specific function signature, output format, or return type that the test will check. A learner who understands the concept but builds a slightly different interface (e.g., prints instead of returns, writes CSV instead of plain text) will fail the test.

**Fix pattern:** End each tutorial section with a "Your task" paragraph that explicitly states: "Your function is `X(params)`, it must return `Y`, and must print `Z` to stdout." Anchor the concept to the specific contract.

---

## Prioritized Fix List

### CRITICAL — Sprint 26 must address these

| # | Quest | Fix needed |
|---|---|---|
| C1 | `python-loop` | Rewrite briefing + tutorial to describe `generate_evens(limit) -> list[int]`. Replace hint 3 (print-based full solution) with staged hint about list accumulation. |
| C2 | `python-data-forge` | Rewrite briefing, tutorial, hints, and example.py to describe the CSV sales pipeline (`load_sales`, `revenue_by_item`, `top_items`). Tutorial needs: `csv.DictReader`, float casting, dict accumulation. |
| C3 | `python-systems-platform-tooling` | Preferred: replace `main.py` stub + grading tests with the `slugify`/`unique_sorted`/`run_tool_request` task the existing docs describe. Alternative: rewrite docs/tutorial/hints/example for `parse_semver`. |
| C4 | `python-boss-csv-report` | Rewrite `briefing.md` to fully specify: input schema (`id`, `sales`), output format (plain text `KEY=VALUE` lines), stdout sentinels (`REPORT_GENERATED`, `INPUT_MISSING`). Update example.py to match. Rewrite hint 3 (remove `fieldnames` advice). |

### IMPORTANT — Sprint 26 should address these

| # | Quest | Fix needed |
|---|---|---|
| I1 | `python-systems-performance-profile` | Rewrite tutorial.md (Counter + regex tokenization + sort key). Rewrite all 3 hints for `most_common_tokens`. |
| I2 | `python-systems-observability-sli` | Replace all 3 hints with hints for `calculate_availability`. Fix `example.py` field name (`status` → `status_code`). |
| I3 | `python-systems-service-boundaries` | Fix tutorial: replace mutable-mutation example with `dataclasses.replace()`. Add frozen-dataclass note to hint 2 or 3. |
| I4 | `python-functions-contracts` | Add `"active": True` to briefing output spec and tutorial return example. Add negative-age rule to briefing. Update hint 3. |
| I5 | `python-oop-mini` | Add to briefing: "`deposit` and `withdraw` raise `ValueError` if amount ≤ 0." Add to tutorial. Update hints. |
| I6 | `python-cli-args` | Add to briefing: default output is `"Hello World"` repeated `count` times; `--verbose` prints `"Processing {i}/{count}..."` before each. |
| I7 | `selenium-open-page` | Fix hint 3: change `"Mock CMS"` to `"CMS Login"`. |

### POLISH — Sprint 27 or later

| # | Quest | Fix needed |
|---|---|---|
| P1 | `python-systems-resilient-job-runner` | Replace hint 3 (full solution) with a hint about the loop index and `raise X from y`. |
| P2 | `python-dicts-lists-transform` | Replace `example.py` with a different aggregation problem (different column names) to preserve pedagogical gap. |
| P3 | `python-file-io-safe` | Add `from pathlib import Path` to `task.py` stub scaffold. |
| P4 | `selenium-find-elements` | Update briefing to mention all three elements (username, password, submit). |
| P5 | `first-sparks` | Add one sentence on f-strings to tutorial, or show both concatenation and f-string in the hint. |

---

## Out of Scope for Sprint 26

These were noticed during the audit but are not pedagogical issues:

**Infrastructure:**
- DinD path resolution prevents live SUBMIT verification for `mode=tests` quests (all python-systems, python-ignition). Documented in `PLATFORM_ARCHITECTURE_AUDIT.md` Sprint 25 backlog note.

**Residual Sprint 24 naming drift:**
- `python-systems-resilient-job-runner` questpack JSON `briefing_md` still describes `run_jobs` / `TransientError` / `FatalError` while the workspace uses `run_with_retries`. The disk `docs/briefing.md` file (which takes priority) is correct — this is a questpack JSON stale field only.
- `python-systems-observability-sli` questpack JSON description says "success rate, error rate, p95 latency" (the old complex function). Disk briefing is correct.

**Example-is-solution convention:**
- The Selenium track deliberately uses reference-solution `example.py` files. This is appropriate for Selenium (WebDriver boilerplate is high) but creates a copy-paste path in Python function quests. The convention decision (when is a reference solution appropriate?) is a curriculum design question beyond one sprint of fixes.

**`task.py` vs `main.py` naming:**
- Selenium quests use `main.py` as the learner file; tier-2 quests use `task.py`. This is intentional (scripts vs. functions) but not documented anywhere. A new quest author would have no guidance on which to use.
