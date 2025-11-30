import asyncio
import os
from arcade_app.grading_helper import grade_submission
from arcade_app.coach_helper import generate_coach_feedback

async def run_scenario(name, input_code, expected_snippet):
    print(f"\n🧪 Testing Scenario: {name}")
    print(f"   Input: {input_code}")
    
    # 1. Grade
    print("   ... Grading ...")
    grade = await grade_submission(model=None, user_input=input_code, track="debugging")
    score = grade.get("weighted_score", 0)
    print(f"   Score: {score}")
    
    # 2. Coach
    print("   ... Coaching ...")
    feedback = await generate_coach_feedback(user_input=input_code, grade=grade, track="debugging")
    print(f"   Feedback: {feedback}")
    
    # 3. Verify
    if expected_snippet in feedback:
        print("   ✅ PASS: Feedback contains expected text.")
    else:
        print(f"   ❌ FAIL: Expected '{expected_snippet}' not found.")

async def main():
    print(f"🚀 Starting Coach Smoke Test (Mock Mode: {os.getenv('EVALFORGE_MOCK_GRADING')})...")
    
    # Scenario A: Success (High Score)
    await run_scenario(
        "Success (High Score)",
        "const x = 1; // Correct code",
        "🎉 **Excellent work!**"
    )
    
    # Scenario B: Failure (Low Score)
    await run_scenario(
        "Failure (Low Score)",
        "function add(a,b) { return a-b; }",
        "🛑 **Let's pause.**"
    )
    
    # Scenario C: Warning (Mid Score)
    await run_scenario(
        "Warning (Mid Score)",
        "def calculate_total(items): return sum(items)",
        "🤔 **Good start.**"
    )

if __name__ == "__main__":
    asyncio.run(main())
