from runner import run_code
from ollama_client import ask_ollama

MAX_ATTEMPTS = 5

current_file = "sample_bug.py"

for attempt in range(1, MAX_ATTEMPTS + 1):

    print(f"\n===== ATTEMPT {attempt} =====")

    result = run_code(current_file)

    if result["success"]:
        print("\n✅ Bug fixed successfully!")
        print(result["stdout"])
        break

    with open(current_file, "r") as f:
        code = f.read()

    prompt = f"""
You are an expert Python debugging agent.

The previous version failed.

Rules:
1. Do NOT change input values.
2. Do NOT remove functionality.
3. Only fix the bug.
4. Return ONLY Python code.
5. No explanations.
6. No markdown.

Code:
{code}

Error:
{result['stderr']}
"""

    fixed_code = ask_ollama(prompt)

    fixed_code = fixed_code.replace("```python", "")
    fixed_code = fixed_code.replace("```", "")
    fixed_code = fixed_code.strip()

    with open("fixed_code.py", "w") as f:
        f.write(fixed_code)

    current_file = "fixed_code.py"

    print("\nGenerated Fix:")
    print(fixed_code)

else:
    print("\n❌ Agent failed after maximum attempts.")