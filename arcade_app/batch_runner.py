import asyncio
import json
import os
import time
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass

# Import your core logic
from arcade_app.grading_helper import grade_submission

RUNS_DIR = "runs"
DATASET_PATH = "data/golden_dataset.jsonl"

@dataclass
class EvalResult:
    case_id: str
    track: str
    score: float
    latency_ms: float
    passed: bool

class BatchRunner:
    def __init__(self, dataset_path: str = DATASET_PATH):
        self.dataset_path = dataset_path
        self.results: List[EvalResult] = []
        self.model = None  # Placeholder for real model if needed

        # Ensure run directory exists
        os.makedirs(RUNS_DIR, exist_ok=True)

        # Log active mode
        is_mock = os.getenv("EVALFORGE_MOCK_GRADING", "0") == "1"
        print(f"🔧 Batch Runner Initialized. Mode: {'MOCK' if is_mock else 'REAL'}")

    def load_dataset(self) -> List[Dict]:
        """Reads the JSONL dataset."""
        data = []
        if not os.path.exists(self.dataset_path):
            print(f"❌ Dataset not found: {self.dataset_path}")
            return []
            
        with open(self.dataset_path, "r") as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data

    async def run(self):
        cases = self.load_dataset()
        print(f"🚀 Starting run with {len(cases)} cases...")
        
        start_time = time.time()
        
        for case in cases:
            # Timing the execution
            t0 = time.time()
            
            # Call the Grading Helper directly
            # Note: We pass None as model if using Mock, or real model otherwise
            result = await grade_submission(
                model=self.model, 
                user_input=case["input"], 
                track=case.get("track", "default")
            )
            
            duration_ms = (time.time() - t0) * 1000
            
            # Simple Pass/Fail logic (e.g., must be within 10 points of expected)
            expected = case.get("expected_score", 0)
            actual = result["weighted_score"]
            passed = abs(actual - expected) <= 10  # Tolerance threshold

            print(f"   [{case['id']}] Score: {actual} (Exp: {expected}) | {duration_ms:.0f}ms | {'✅' if passed else '❌'}")

            self.results.append(EvalResult(
                case_id=case["id"],
                track=case.get("track", "default"),
                score=actual,
                latency_ms=duration_ms,
                passed=passed
            ))

        total_duration = time.time() - start_time
        self._save_run(total_duration)

    def _save_run(self, duration_sec: float):
        """Serializes the run to a JSON file."""
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filename = os.path.join(RUNS_DIR, f"{run_id}.json")
        
        # Calculate summary stats
        avg_score = sum(r.score for r in self.results) / len(self.results) if self.results else 0
        pass_rate = sum(1 for r in self.results if r.passed) / len(self.results) if self.results else 0

        output = {
            "meta": {
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "duration_sec": round(duration_sec, 2),
                "mock_mode": os.getenv("EVALFORGE_MOCK_GRADING") == "1"
            },
            "summary": {
                "total_cases": len(self.results),
                "avg_score": round(avg_score, 1),
                "pass_rate_pct": round(pass_rate * 100, 1)
            },
            "results": [
                {
                    "id": r.case_id,
                    "score": r.score,
                    "latency": round(r.latency_ms, 1),
                    "passed": r.passed
                }
                for r in self.results
            ]
        }

        with open(filename, "w") as f:
            json.dump(output, f, indent=2)
            
        print(f"\n💾 Run saved to: {filename}")
        print(f"📊 Summary: Avg Score: {avg_score:.1f} | Pass Rate: {pass_rate:.0%}")

if __name__ == "__main__":
    runner = BatchRunner()
    asyncio.run(runner.run())
