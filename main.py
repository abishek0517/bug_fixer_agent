import json
import os
from datetime import datetime

from runner import run_code
from ollama_client import ask_ollama

MAX_ATTEMPTS = 5
HISTORY_FILE = "bug_history.json"

current_file = "sample_bug.py"
previous_attempts = []

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
run_folder = f"attempts/run_{run_id}"
os.makedirs(run_folder, exist_ok=True)


def save_history(record):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    history.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


for attempt in range(1, MAX_ATTEMPTS + 1):

    print(f"\n===== ATTEMPT {attempt} =====")

    result = run_code(current_file)

    if result["success"]:
        print("\n✅ Bug fixed successfully!")
        print(result["stdout"])

        save_history({
            "run_id": run_id,
            "run_folder": run_folder,
            "original_file": "sample_bug.py",
            "final_file": current_file,
            "success": True,
            "attempts": previous_attempts,
            "finished_at": datetime.now().isoformat()
        })

        break

    with open(current_file, "r") as f:
        code = f.read()

    previous_attempts_text = ""

    for index, previous in enumerate(previous_attempts, start=1):
        previous_attempts_text += f"""
Previous Attempt {index}:

Code:
{previous["code"]}

Error:
{previous["error"]}
"""

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
7. Do NOT repeat previous attempts.

Previous attempts:
{previous_attempts_text}

Current code:
{code}

Current error:
{result['stderr']}
"""

    fixed_code = ask_ollama(prompt)

    if fixed_code is None:
        print("\nOllama is not available or did not return a response.")

        save_history({
            "run_id": run_id,
            "run_folder": run_folder,
            "original_file": "sample_bug.py",
            "final_file": current_file,
            "success": False,
            "reason": "Ollama did not return a response",
            "attempts": previous_attempts,
            "finished_at": datetime.now().isoformat()
        })

        break

    fixed_code = fixed_code.replace("```python", "")
    fixed_code = fixed_code.replace("```", "")
    fixed_code = fixed_code.strip()

    attempt_file = f"{run_folder}/attempt_{attempt}.py"

    with open(attempt_file, "w") as f:
        f.write(fixed_code)

    previous_attempts.append({
        "attempt": attempt,
        "file": attempt_file,
        "code": fixed_code,
        "error": result["stderr"]
    })

    current_file = attempt_file

    print("\nGenerated Fix:")
    print(fixed_code)
    print(f"\nSaved attempt to: {attempt_file}")

else:
    print("\n❌ Agent failed after maximum attempts.")

    save_history({
        "run_id": run_id,
        "run_folder": run_folder,
        "original_file": "sample_bug.py",
        "final_file": current_file,
        "success": False,
        "reason": "Maximum attempts reached",
        "attempts": previous_attempts,
        "finished_at": datetime.now().isoformat()
    })