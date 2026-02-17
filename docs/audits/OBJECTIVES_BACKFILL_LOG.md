# Objectives Backfill Log

Track of quest-by-quest backfill progress with golden captures and verification results.

---

## python-loop

**Date:** 2026-02-17

**Objectives Added:**
1. `obj_define_function` (ast: must_define_function="generate_evens")
2. `obj_stdout` (stdout_exact: pattern="2,4,6,8,10") 
3. `obj_tests` (tests_pass)

**Golden Capture:**
- Type: **RUN** ✅
- stdout: `"2,4,6,8,10\r\n"`
- stdout_sha256: `064c6e5100b244ac...`
- exit_code: 0
- File: `data/quests/python-loop/grading/golden.json`

**Solution Fixed:**
- Original solution had wrong function name (`process_numbers` vs `generate_evens`)
- Updated to match task requirements
- Fixed test file to import correct function

**Verified:**
- ✅ Golden capture successful
- ⏳ Pending: Re-seed and UI validation

**Notes:**
Quest teaches for loops by having students generate even numbers from 2 to limit. Main function prints comma-separated output.

---

## python-data-forge

**Date:** 2026-02-17

**Objectives Added:**
1. `obj_load_sales` (ast: must_define_function="load_sales")
2. `obj_revenue_by_item` (ast: must_define_function="revenue_by_item")
3. `obj_top_items` (ast: must_define_function="top_items")
4. `obj_stdout` (stdout_regex: pattern for "apple=10.50\nbanana=6.40")

**Golden Capture:**
- Type: **SPEC** 📋 (blocked by missing fixtures in run workspace)
- Expected stdout: `"apple=10.50\nbanana=6.40\n"`
- Calculation: Based on fixtures/sales.csv aggregation
- File: `data/quests/python-data-forge/grading/golden.spec.json`

**Blocked Reason:**
Solution requires CSV fixtures (`fixtures/sales.csv`) which aren't available in temp run workspace. Need workspace packaging to include fixtures.

**TODO:**
- [ ] Implement fixture packaging in runner
- [ ] Convert to golden.run.json once unblocked

**Verified:**
- ✅ Golden spec created with expected output
- ✅ Objectives designed from spec
- ⏳ Pending: Re-seed validation

**Notes:**
Quest teaches CSV parsing, dictionary aggregation, and custom sorting. More complex than python-loop - good boss-prep difficulty.

---
