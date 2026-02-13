import shutil
from pathlib import Path
import textwrap

# Configuration
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_QUESTS = REPO_ROOT / "data" / "quests"
SHARED_HELPERS = REPO_ROOT / "data" / "_shared"

QUESTS = [
    # Foundry
    {
        "slug": "python-loop",
        "readme": "# Python Loop\n\nImplement `process_numbers(nums)` that returns a list of even numbers multiplied by 2.",
        "starter": "def process_numbers(nums):\n    return []",
        "solution": "def process_numbers(nums):\n    return [n * 2 for n in nums if n % 2 == 0]",
        "test": """
import pytest
from main import process_numbers

def test_process_numbers():
    assert process_numbers([1, 2, 3, 4]) == [4, 8]
    assert process_numbers([1, 3, 5]) == []
    assert process_numbers([]) == []
"""
    },
    {
        "slug": "python-data-forge",
        "readme": "# Data Forge\n\nImplement `forge_data(users)`.\nInput: list of `{'id': int, 'name': str, 'active': bool}`.\nOutput: dict mapping ID to Name for ACTIVE users only.",
        "starter": "def forge_data(users):\n    return {}",
        "solution": "def forge_data(users):\n    return {u['id']: u['name'] for u in users if u.get('active')}",
        "test": """
import pytest
from main import forge_data

def test_forge_data():
    in_data = [
        {'id': 1, 'name': 'Alice', 'active': True},
        {'id': 2, 'name': 'Bob', 'active': False},
        {'id': 3, 'name': 'Charlie', 'active': True}
    ]
    out = forge_data(in_data)
    assert out == {1: 'Alice', 3: 'Charlie'}
    assert 2 not in out
"""
    },
    # Systems
    {
        "slug": "python-systems-service-boundaries",
        "readme": "# Service Boundaries\n\nDefine a class `PaymentService`.\nIt should have a method `process(amount)`.\nIf amount < 0, raise `ValueError`. Else return `True`.",
        "starter": "class PaymentService:\n    pass",
        "solution": "class PaymentService:\n    def process(self, amount):\n        if amount < 0: raise ValueError('Negative')\n        return True",
        "test": """
import pytest
from main import PaymentService

def test_payment_service():
    svc = PaymentService()
    assert svc.process(100) is True
    with pytest.raises(ValueError):
        svc.process(-1)
"""
    },
    {
        "slug": "python-systems-resilient-job-runner",
        "readme": "# Resilient Job Runner\n\nImplement `run_with_retry(fn, max_retries)`.\nExecutes `fn()`. If it raises exception, retry up to `max_retries`.\nIf all fail, raise the last exception.",
        "starter": "def run_with_retry(fn, max_retries=3):\n    pass",
        "solution": """
def run_with_retry(fn, max_retries=3):
    last_exc = None
    for _ in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
    raise last_exc
""",
        "test": """
import pytest
from unittest.mock import Mock
from main import run_with_retry

def test_success():
    m = Mock(return_value="ok")
    assert run_with_retry(m, 3) == "ok"
    assert m.call_count == 1

def test_retry_success():
    m = Mock(side_effect=[Exception("fail"), "ok"])
    assert run_with_retry(m, 3) == "ok"
    assert m.call_count == 2

def test_fail_all():
    m = Mock(side_effect=ValueError("boom"))
    with pytest.raises(ValueError):
        run_with_retry(m, 2)
    assert m.call_count == 3
"""
    },
    {
        "slug": "python-systems-observability-sli",
        "readme": "# Observability SLI\n\nImplement `calculate_sli(good, total)`.\nReturn `good / total` as float.\nIf total is 0, return 1.0.",
        "starter": "def calculate_sli(good, total):\n    return 0.0",
        "solution": "def calculate_sli(good, total):\n    if total == 0: return 1.0\n    return float(good) / total",
        "test": """
import pytest
from main import calculate_sli

def test_sli():
    assert calculate_sli(99, 100) == 0.99
    assert calculate_sli(0, 0) == 1.0
    assert calculate_sli(50, 100) == 0.5
"""
    },
    {
        "slug": "python-systems-performance-profile",
        "readme": "# Performance Profile\n\nImplement `profile_matrix(n)` that returns an `n x n` identity matrix (list of lists).\nOptimize for readability.",
        "starter": "def profile_matrix(n):\n    return []",
        "solution": "def profile_matrix(n):\n    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]",
        "test": """
import pytest
from main import profile_matrix

def test_matrix():
    assert profile_matrix(2) == [[1, 0], [0, 1]]
    assert profile_matrix(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
"""
    },
    {
        "slug": "python-systems-platform-tooling",
        "readme": "# Platform Tooling\n\nImplement `parse_semver(version_str)`.\nReturn tuple `(major, minor, patch)` as ints.\nRaise ValueError if invalid format `x.y.z`.",
        "starter": "def parse_semver(v):\n    return (0, 0, 0)",
        "solution": """
def parse_semver(v):
    parts = v.split('.')
    if len(parts) != 3: raise ValueError("Invalid format")
    try:
        return tuple(map(int, parts))
    except:
        raise ValueError("Not integers")
""",
        "test": """
import pytest
from main import parse_semver

def test_semver():
    assert parse_semver("1.2.3") == (1, 2, 3)
    with pytest.raises(ValueError):
        parse_semver("1.2")
    with pytest.raises(ValueError):
        parse_semver("a.b.c")
"""
    }
]

def scaffold_quest(q):
    slug = q["slug"]
    print(f"Scaffolding {slug}...")
    
    quest_dir = DATA_QUESTS / slug
    quest_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Workspace
    (quest_dir / "workspace").mkdir(exist_ok=True)
    (quest_dir / "workspace" / "README.md").write_text(q["readme"], encoding="utf-8")
    
    (quest_dir / "workspace" / "main.py").write_text(q["starter"], encoding="utf-8")
    
    
    # 2. Cleaning
    grading_dir = quest_dir / "grading"
    if grading_dir.exists():
        shutil.rmtree(grading_dir)
    
    # Re-create
    (quest_dir / "grading" / "public").mkdir(parents=True, exist_ok=True)
    (quest_dir / "grading" / "solutions").mkdir(parents=True, exist_ok=True)
    
    (quest_dir / "grading" / "public" / f"test_{slug.replace('-', '_')}.py").write_text(q["test"].strip(), encoding="utf-8")
    (quest_dir / "grading" / "solutions" / "main.py").write_text(q["solution"].strip(), encoding="utf-8")

def main():
    for q in QUESTS:
        scaffold_quest(q)
    print("Scaffolded 7 Python quests.")

if __name__ == "__main__":
    main()
