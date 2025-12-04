#!/usr/bin/env python
"""
Simple test to verify boss QA components are wired correctly.
Tests rubric loading and scoring logic without full database.
"""
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Enable mock mode
os.environ["EVALFORGE_MOCK_GRADING"] = "1"


def test_rubric_loading():
    """Test that rubrics can be loaded."""
    from arcade_app.boss_rubric_helper import load_boss_rubric
    
    print("Testing rubric loading...")
    
    try:
        # Test runtime boss rubric
        runtime_rubric = load_boss_rubric("applylens-runtime")
        print(f"✓ Loaded runtime rubric: {runtime_rubric.title}")
        print(f"  - Dimensions: {len(runtime_rubric.dimensions)}")
        print(f"  - Max Score: {runtime_rubric.max_score}")
        
        # Test agent boss rubric  
        agent_rubric = load_boss_rubric("applylens-agent")
        print(f"✓ Loaded agent rubric: {agent_rubric.title}")
        print(f"  - Dimensions: {len(agent_rubric.dimensions)}")
        print(f"  - Autofail Conditions: {agent_rubric.autofail_conditions}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load rubrics: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mock_evaluation():
    """Test mock boss evaluation."""
    from arcade_app.boss_rubric_helper import load_boss_rubric, score_boss_eval
    from arcade_app.boss_rubric_models import BossEvalLLMChoice, BossEvalDimensionChoice
    
    print("\nTesting mock evaluation...")
    
    try:
        rubric = load_boss_rubric("applylens-runtime")
        
        # Create mock ZERO response
        choice = BossEvalLLMChoice(
            dimensions=[
                BossEvalDimensionChoice(key="slo_and_metrics", level=2, rationale="Good SLO definition"),
                BossEvalDimensionChoice(key="observability_pipeline", level=2, rationale="Layered observability"),
                BossEvalDimensionChoice(key="failure_handling", level=1, rationale="Basic retries"),
                BossEvalDimensionChoice(key="idempotency_and_consistency", level=1, rationale="Basic guards"),
                BossEvalDimensionChoice(key="alerts_and_response", level=1, rationale="Some alerts"),
                BossEvalDimensionChoice(key="load_testing_and_drills", level=0, rationale="Not tested"),
            ],
            autofail_conditions_triggered=[]
        )
        
        # Score it
        result = score_boss_eval(rubric, choice)
        
        print(f"✓ Evaluation complete:")
        print(f"  - Score: {result.total_score} / {result.max_score}")
        print(f"  - Grade: {result.grade}")
        print(f"  - Dimensions evaluated: {len(result.dimensions)}")
        
        return True
    except Exception as e:
        print(f"✗ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("ApplyLens Boss QA - Component Test")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test rubric loading
    if not test_rubric_loading():
        all_passed = False
    
    # Test evaluation
    if not test_mock_evaluation():
        all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ All component tests passed!")
        print("=" * 60)
        return 0
    else:
        print("❌ Some tests failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
