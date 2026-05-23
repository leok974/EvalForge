# Briefing: BOSS: CSV Reporter

## The Mission
Congratulations, Agent. You've been promoted to lead the Data Logistics division. Your first major task is to automate our weekly resource reports. We receive raw CSV files containing telemetry from the outer sectors, and we need a tool that can parse these files, aggregate the data, and generate a clean summary report.

This is a **BOSS LEVEL** quest. You must combine everything you've learned about Python file handling, logic, and data structures.

## Objectives
- Implement `generate_report(input_csv, output_report)`:
  - **Read**: Load the data from `input_csv` using Python's `csv` module.
  - **Process**: Calculate summary statistics (e.g., total volume, average temperature, or counts by sector).
  - **Write**: Save the resulting summary to `output_report` (which should be `report.csv`).
- Requirements:
  - Your script must use the `csv` module for both reading and writing.
  - Handle potential errors like missing files or malformed CSV rows.
  - The report must be deterministic and match the expected format.

## Constraints
- Do not use `pandas`. Use only the standard library.
- The entrypoint is `task.py`.
