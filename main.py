from datetime import datetime

from runner import run_code
from ollama_client import ask_ollama
from tools import (
    read_file,
    create_run_folder,
    save_history,
    create_history_record,
    clean_model_response,
    is_valid_python,
    save_attempt,
    create_attempt_memory,
    build_prompt,
    keep_original_test_code
)

MAX_ATTEMPTS = 5
HISTORY_FILE = "bug_history.json"
ORIGINAL_FILE = "sample_bug.py"

current_file = ORIGINAL_FILE
previous_attempts = []

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
run_folder = create_run_folder(run_id)
original_code = read_file(ORIGINAL_FILE)


for attempt in range(1, MAX_ATTEMPTS + 1):

    print(f"\n===== ATTEMPT {attempt} =====")

    result = run_code(current_file)

    if result["success"]:
        print("\nSUCCESS: Bug fixed successfully!")
        print(result["stdout"])

        record = create_history_record(
            run_id=run_id,
            run_folder=run_folder,
            original_file=ORIGINAL_FILE,
            original_code=original_code,
            final_file=current_file,
            success=True,
            attempts=previous_attempts,
            finished_at=datetime.now().isoformat()
        )

        save_history(HISTORY_FILE, record)
        break

    code = read_file(current_file)

    prompt = build_prompt(
        code,
        result["stderr"],
        previous_attempts
    )

    fixed_code = ask_ollama(prompt)

    if fixed_code is None:
        print("\nOllama is not available or did not return a response.")

        record = create_history_record(
            run_id=run_id,
            run_folder=run_folder,
            original_file=ORIGINAL_FILE,
            original_code=original_code,
            final_file=current_file,
            success=False,
            attempts=previous_attempts,
            finished_at=datetime.now().isoformat(),
            reason="Ollama did not return a response"
        )

        save_history(HISTORY_FILE, record)
        break

    fixed_code = clean_model_response(fixed_code)

    if not fixed_code:
        print("\nModel returned empty code.")

        record = create_history_record(
            run_id=run_id,
            run_folder=run_folder,
            original_file=ORIGINAL_FILE,
            original_code=original_code,
            final_file=current_file,
            success=False,
            attempts=previous_attempts,
            finished_at=datetime.now().isoformat(),
            reason="Model returned empty code"
        )

        save_history(HISTORY_FILE, record)
        break

    fixed_code = keep_original_test_code(original_code, fixed_code)

    attempt_file = save_attempt(run_folder, attempt, fixed_code)

    valid_python, syntax_error = is_valid_python(attempt_file)

    if not valid_python:
        print("\nGenerated code is not valid Python.")
        print(syntax_error)

        previous_attempts.append(
            create_attempt_memory(
                attempt_number=attempt,
                attempt_file=attempt_file,
                code=fixed_code,
                error=syntax_error
            )
        )

        continue

    previous_attempts.append(
        create_attempt_memory(
            attempt_number=attempt,
            attempt_file=attempt_file,
            code=fixed_code,
            error=result["stderr"]
        )
    )

    current_file = attempt_file

    print("\nGenerated Fix:")
    print(fixed_code)
    print(f"\nSaved attempt to: {attempt_file}")

else:
    print("\nFAILED: Agent failed after maximum attempts.")

    record = create_history_record(
        run_id=run_id,
        run_folder=run_folder,
        original_file=ORIGINAL_FILE,
        original_code=original_code,
        final_file=current_file,
        success=False,
        attempts=previous_attempts,
        finished_at=datetime.now().isoformat(),
        reason="Maximum attempts reached"
    )

    save_history(HISTORY_FILE, record)