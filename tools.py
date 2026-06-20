import json
import os
import py_compile


TEST_MARKER = "# === TESTS ==="


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


def create_run_folder(run_id):
    run_folder = f"attempts/run_{run_id}"
    os.makedirs(run_folder, exist_ok=True)
    return run_folder


def load_history(history_file):
    if not os.path.exists(history_file):
        return []

    try:
        with open(history_file, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history_file, record):
    history = load_history(history_file)
    history.append(record)

    with open(history_file, "w") as file:
        json.dump(history, file, indent=4)


def create_history_record(
    run_id,
    run_folder,
    original_file,
    original_code,
    final_file,
    success,
    attempts,
    finished_at,
    reason=None
):
    record = {
        "run_id": run_id,
        "run_folder": run_folder,
        "original_file": original_file,
        "original_code": original_code,
        "final_file": final_file,
        "success": success,
        "attempts": attempts,
        "finished_at": finished_at
    }

    if reason is not None:
        record["reason"] = reason

    return record


def clean_model_response(response):
    cleaned_response = response.replace("```json", "")
    cleaned_response = cleaned_response.replace("```python", "")
    cleaned_response = cleaned_response.replace("```", "")
    return cleaned_response.strip()


def parse_model_response(response):
    cleaned_response = clean_model_response(response)

    try:
        data = json.loads(cleaned_response)
    except json.JSONDecodeError:
        return None

    required_fields = [
        "bug_type",
        "explanation",
        "fixed_code",
        "confidence"
    ]

    for field in required_fields:
        if field not in data:
            return None

    return data


def is_valid_python(filename):
    try:
        py_compile.compile(filename, doraise=True)
        return True, ""
    except py_compile.PyCompileError as error:
        return False, str(error)


def save_attempt(run_folder, attempt_number, fixed_code):
    attempt_file = f"{run_folder}/attempt_{attempt_number}.py"
    write_file(attempt_file, fixed_code)
    return attempt_file


def create_attempt_memory(
    attempt_number,
    attempt_file,
    code,
    error,
    bug_type=None,
    explanation=None,
    confidence=None
):
    memory = {
        "attempt": attempt_number,
        "file": attempt_file,
        "code": code,
        "error": error
    }

    if bug_type is not None:
        memory["bug_type"] = bug_type

    if explanation is not None:
        memory["explanation"] = explanation

    if confidence is not None:
        memory["confidence"] = confidence

    return memory


def get_function_code(code):
    if TEST_MARKER not in code:
        return code.strip()

    return code.split(TEST_MARKER, 1)[0].strip()


def get_test_code(code):
    if TEST_MARKER not in code:
        return ""

    test_code = code.split(TEST_MARKER, 1)[1].strip()
    return TEST_MARKER + "\n\n" + test_code


def keep_original_test_code(original_code, fixed_code):
    fixed_function_code = get_function_code(fixed_code)
    original_test_code = get_test_code(original_code)

    return fixed_function_code + "\n\n" + original_test_code


def test_code_changed(original_code, fixed_code):
    original_test_code = get_test_code(original_code)
    fixed_test_code = get_test_code(fixed_code)

    return original_test_code != fixed_test_code


def build_prompt(code, error, previous_attempts):
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

The Python program failed its locked tests.
Use the test failure to understand the expected behavior.

Return only valid JSON using this exact structure:

{{
    "bug_type": "type of bug",
    "explanation": "short explanation of the bug",
    "fixed_code": "complete corrected Python code",
    "confidence": 0.0
}}

Rules:
1. Only fix the Python code above the test marker.
2. Do NOT change code below the test marker.
3. Do NOT change test inputs or expected outputs.
4. Do NOT remove functionality.
5. Return only valid JSON.
6. Do NOT use markdown.
7. Do NOT repeat previous attempts.
8. Confidence must be a number from 0.0 to 1.0.

Previous attempts:
{previous_attempts_text}

Current code:
{code}

Current error:
{error}
"""

    return prompt