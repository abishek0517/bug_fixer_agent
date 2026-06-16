# Auto Bug Fixer Agent

An Agentic AI project that automatically detects, analyzes, and fixes Python runtime errors using a local LLM powered by Ollama and Llama 3.

## Features

* Executes Python code
* Captures runtime errors
* Sends code and error details to a local LLM
* Generates corrected code
* Saves the fix automatically
* Validates the fix by rerunning the code

## Tech Stack

* Python 3.13
* Ollama
* Llama 3
* Requests

## Project Workflow

1. Execute buggy Python code
2. Capture error output
3. Send code and error to Llama 3
4. Generate a fix
5. Save corrected code
6. Re-run code to verify success

## Example

Input:

```python
def divide(a, b):
    return a / b

print(divide(10, 0))
```

Output:

```python
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    else:
        return a / b

print(divide(10, 0))
```

## Future Improvements

* Self-retrying agent loops
* Reflection and memory
* Unit test generation
* Git integration
* Multi-file project debugging
