# furnace_controller.py

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Iterable, List


logger = logging.getLogger(__name__)


def configure_logging(level: str = "INFO") -> None:
    """Configure basic logging for the CLI."""
    numeric = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Furnace Controller")
    parser.add_argument("--input", required=True, help="Path to sensor JSON file")
    parser.add_argument(
        "--target-temp",
        type=float,
        required=True,
        help="Target temperature in Celsius",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1.0,
        help="Allowed deviation from target before action is taken",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    return parser.parse_args(argv)


def load_sensor_data(path: Path) -> List[float]:
    """Load sensor readings from a JSON file.

    Expected format:
        {"readings": [21.0, 22.5, 20.8]}
    """
    if not path.is_file():
        raise FileNotFoundError(f"Sensor file not found: {path}")

    with path.open("r", encoding="utf8") as f:
        try:
            payload = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {path}") from exc

    readings = payload.get("readings")
    if not isinstance(readings, list) or not readings:
        raise ValueError("JSON must contain a non-empty 'readings' list")

    cleaned: List[float] = []
    for raw in readings:
        try:
            cleaned.append(float(raw))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid reading {raw!r} in {path}") from exc

    return cleaned


def compute_average(readings: Iterable[float]) -> float:
    values = list(readings)
    if not values:
        raise ValueError("Cannot compute average of empty readings")
    return sum(values) / len(values)


def decide_action(
    avg_temp: float, target_temp: float, tolerance: float
) -> str:
    """Decide whether to HEAT, COOL, or STABLE based on target and tolerance."""
    lower = target_temp - tolerance
    upper = target_temp + tolerance

    if avg_temp < lower:
        return "HEAT"
    if avg_temp > upper:
        return "COOL"
    return "STABLE"


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.log_level)

    sensor_path = Path(args.input)

    logger.info("Starting Furnace Controller")
    logger.info("Sensor file: %s", sensor_path)
    logger.info(
        "Target=%.2f°C, tolerance=±%.2f°C",
        args.target_temp,
        args.tolerance,
    )

    try:
        readings = load_sensor_data(sensor_path)
        avg = compute_average(readings)
    except Exception as exc:
        logger.error("Failed to load/compute readings: %s", exc)
        return 1

    logger.info("Average temperature: %.2f°C", avg)
    action = decide_action(avg, args.target_temp, args.tolerance)
    logger.info("Decision: %s", action)

    # Exit codes: 0=stable, 10=heat, 11=cool
    if action == "HEAT":
        return 10
    if action == "COOL":
        return 11
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
