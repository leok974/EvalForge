# data_crucible.py

from __future__ import annotations

import argparse
import csv
import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List


logger = logging.getLogger(__name__)


@dataclass
class CrucibleConfig:
    group_by: List[str]
    value_field: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CrucibleConfig":
        if "group_by" not in data or "value_field" not in data:
            raise ValueError("Config must include 'group_by' and 'value_field' keys")

        group_by = data["group_by"]
        if not isinstance(group_by, list) or not all(isinstance(k, str) for k in group_by):
            raise ValueError("'group_by' must be a list of strings")

        value_field = data["value_field"]
        if not isinstance(value_field, str):
            raise ValueError("'value_field' must be a string")

        return cls(group_by=group_by, value_field=value_field)


def configure_logging(level: str = "INFO") -> None:
    numeric = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data Crucible – config-driven CSV aggregator")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--config", required=True, help="Path to JSON config file")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    parser.add_argument("--log-level", default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR)")
    return parser.parse_args(argv)


def load_config(path: Path) -> CrucibleConfig:
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in config file {path}") from exc

    return CrucibleConfig.from_dict(raw)


def load_rows(path: Path) -> List[Dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"Input CSV file not found: {path}")

    with path.open("r", encoding="utf8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("Input CSV has no data rows")

    return rows


def aggregate(
    rows: Iterable[Dict[str, str]],
    group_by: List[str],
    value_field: str,
) -> List[Dict[str, Any]]:
    """Aggregate numeric value_field by group_by keys using sum + count."""
    totals: Dict[tuple, float] = defaultdict(float)
    counts: Dict[tuple, int] = defaultdict(int)

    for row in rows:
        try:
            key = tuple(row[k] for k in group_by)
        except KeyError as exc:
            raise ValueError(f"Missing group_by column {exc!s} in row: {row}") from exc

        if value_field not in row:
            raise ValueError(f"Missing value_field '{value_field}' in row: {row}")

        try:
            value = float(row[value_field])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid numeric value for '{value_field}' in row: {row}") from exc

        totals[key] += value
        counts[key] += 1

    result: List[Dict[str, Any]] = []
    for key_tuple, total in totals.items():
        count = counts[key_tuple]
        avg = total / count if count else 0.0
        entry: Dict[str, Any] = {group_by[i]: key_tuple[i] for i in range(len(group_by))}
        entry["sum"] = total
        entry["count"] = count
        entry["avg"] = avg
        result.append(entry)

    # Optional: sort by group keys for stable output
    result.sort(key=lambda r: tuple(r[k] for k in group_by))
    return result


def write_output(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf8") as f:
        json.dump(data, f, indent=2, sort_keys=False)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.log_level)

    input_path = Path(args.input)
    config_path = Path(args.config)
    output_path = Path(args.output)

    logger.info("Starting Data Crucible")
    logger.info("Input CSV: %s", input_path)
    logger.info("Config file: %s", config_path)
    logger.info("Output JSON: %s", output_path)

    try:
        config = load_config(config_path)
        rows = load_rows(input_path)
        summary = aggregate(rows, config.group_by, config.value_field)
    except Exception as exc:
        logger.error("Data Crucible failed: %s", exc)
        return 1

    write_output(output_path, summary)
    logger.info("Wrote %d summary rows", len(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
