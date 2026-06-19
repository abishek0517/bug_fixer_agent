import json
import os
import py_compile
from datetime import datetime

from runner import run_code
from ollama_client import ask_ollama

MAX_ATTEMPTS = 5
HISTORY_FILE = "bug_history.json"
ORIGINAL_FILE = "sample_bug.py"

current_file = ORIGINAL_FILE
previous_attempts = []

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
run_folder = f"attempts/run_{run_id}"
os.makedirs(run_folder, exist_ok=True)


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(record):
    history = load_history()
    record["original_code"] = read_file(ORIGINAL_FILE)

    history.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def clean_model_response(response):
    fixed_code = response.replace("```python", "")
    fixed_code = fixed_code.replace("```", "")
    return fixed_code.strip()


def is_valid_python(filename):
    try:
        py_compile.compile(filename, doraise=True)
        return True, ""
    except py_compile.PyCompileError as error:
        return False, str(error)


for attempt in range(1, MAX_ATTEMPTS + 1):

    print(f"\n===== ATTEMPT {attempt} =====")

    result = run_code(current_file)

    if result["success"]:
        print("\nSUCCESS: Bug fixed successfully!")
        print(result["stdout"])

        save_history({
            "run_id": run_id,
            "run_folder": run_folder,
            "original_file": ORIGINAL_FILE,
            "final_file": current_file,
            "success": True,
            "attempts": previous_attempts,
            "finished_at": datetime.now().isoformat()
        })

        break

    code = read_file(current_file)

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
            "original_file": ORIGINAL_FILE,
            "final_file": current_file,
            "success": False,
            "reason": "Ollama did not return a response",
            "attempts": previous_attempts,
            "finished_at": datetime.now().isoformat()
        })

        break

    fixed_code = clean_model_response(fixed_code)

    if not fixed_code:
        print("\nModel returned empty code.")

        save_history({
            "run_id": run_id,
            "run_folder": run_folder,
            "original_file": ORIGINAL_FILE,
            "final_file": current_file,
            "success": False,
            "reason": "Model returned empty code",
            "attempts": previous_attempts,
            "finished_at": datetime.now().isoformat()
        })

        break

    attempt_file = f"{run_folder}/attempt_{attempt}.py"

    with open(attempt_file, "w") as f:
        f.write(fixed_code)

    valid_python, syntax_error = is_valid_python(attempt_file)

    if not valid_python:
        print("\nGenerated code is not valid Python.")
        print(syntax_error)

        previous_attempts.append({
            "attempt": attempt,
            "file": attempt_file,
            "code": fixed_code,
            "error": syntax_error
        })

        continue

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
    print("\nFAILED: Agent failed after maximum attempts.")

    save_history({
        "run_id": run_id,
        "run_folder": run_folder,
        "original_file": ORIGINAL_FILE,
        "final_file": current_file,
        "success": False,
        "reason": "Maximum attempts reached",
        "attempts": previous_attempts,
        "finished_at": datetime.now().isoformat()
    })
