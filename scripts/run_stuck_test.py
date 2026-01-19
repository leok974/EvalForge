import sys
import os

# Add root to path
sys.path.append(os.getcwd())

try:
    from tests.test_stuck_detector import test_stuck_detector_logic, test_coach_response
    print("Running test_stuck_detector_logic...")
    test_stuck_detector_logic()
    print("PASS: test_stuck_detector_logic")
    
    print("Running test_coach_response...")
    test_coach_response()
    print("PASS: test_coach_response")
    
except ImportError as e:
    print(f"Import Error: {e}")
except AssertionError as e:
    print(f"Assertion Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
