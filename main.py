from runner import run_code
from ollama_client import ask_ollama

# Read original code
with open("sample_bug.py", "r") as f:
    code = f.read()

# Run original code
result = run_code("sample_bug.py")

# If code has errors
if not result["success"]:

    prompt = f"""
You are an expert Python debugging agent.

Fix the code based on the error.

Rules:
1. Do NOT change the input values.
2. Do NOT remove functionality.
3. Only fix the bug.
4. Return ONLY executable Python code.
5. No explanations.
6. No markdown.
7. Preserve the original program behavior.

Code:
{code}

Error:
{result['stderr']}
"""

    # Ask Ollama for fix
    fixed_code = ask_ollama(prompt)

    # Clean response
    fixed_code = fixed_code.replace("```python", "")
    fixed_code = fixed_code.replace("```", "")
    fixed_code = fixed_code.replace("Here is the corrected code:", "")
    fixed_code = fixed_code.strip()

    print("\n===== FIXED CODE =====\n")
    print(fixed_code)

    # Save fixed code
    with open("fixed_code.py", "w") as f:
        f.write(fixed_code)

    # Test fixed code
    test_result = run_code("fixed_code.py")

    print("\n===== TEST RESULT =====\n")
    print(test_result)

    if test_result["success"]:
        print("\n✅ Bug fixed successfully!")
    else:
        print("\n❌ Fix failed. More debugging needed.")

else:
    print("✅ Original code already works.")