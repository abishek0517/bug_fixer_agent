# Auto Bug Fixer Agent

A Python-only Agentic AI learning project that detects bugs, asks a local LLM for fixes, saves each attempt, reruns the code, and records history.

The goal of this project is to learn how agents work:

- observe a failure
- ask a model for a fix
- take an action
- test the result
- remember what happened
- retry when needed

## Current Status

Current checkpoint: **Phase 4 completed**

Completed:

- Phase 1: First working bug-fixing loop
- Phase 2: Better agent loop
- Phase 3: Agent memory and history
- Phase 4: Tool-based agent design

Next:

- Start Phase 5: structured reasoning output

Note: A small part of Phase 6 was tested early, but Phase 6 is not complete.

## Learning Workflow

This is a hands-on learning project:

- The student writes and updates the Python code.
- Each new idea is explained briefly in simple language.
- Code is added one small step at a time.
- When a file needs changes, the complete revised file is shown.
- The code is tested after each meaningful step.

## Current Features

- Runs Python code
- Captures stdout, stderr, and success status
- Sends buggy code and error messages to Ollama
- Uses Llama 3 locally
- Handles missing Ollama responses without crashing
- Retries fixes up to a maximum attempt count
- Saves each attempt in a unique run folder
- Stores run history in `bug_history.json`
- Handles empty or broken history files
- Remembers previous attempts during the current run
- Rejects empty model responses
- Checks generated fixes are valid Python before running them
- Uses `tools.py` for reusable agent tools
- Builds prompts through a helper tool
- Saves history records through a helper tool
- Keeps original test code locked while applying generated fixes
- Has fixed simple runtime errors and one experimental logic error

## Project Structure

```text
Auto Bug Fixer Agent
|
|-- sample_bug.py          Buggy Python input file
|-- runner.py              Runs Python files and captures output
|-- ollama_client.py       Talks to local Ollama
|-- tools.py               Reusable agent helper tools
|-- main.py                Main agent loop
|-- bug_history.json       Saved run history
|-- PROJECT_PHASES.txt     Project roadmap
|-- attempts/              Generated fix attempts
```

## How It Works

```text
main.py
|
|-- run the current Python file
|-- if it succeeds, save history and stop
|-- if it fails, read the code
|-- build a prompt with code, error, and previous attempts
|-- ask Ollama for fixed code
|-- clean the model response
|-- keep the original test code locked
|-- save the generated attempt
|-- rerun the generated attempt
|-- repeat until success or max attempts
```

## Requirements

- Python
- Ollama
- Llama 3 model
- requests package

## Run

Start from the project folder:

```powershell
cd C:\Users\abishek\Desktop\PROJECTS\bug_fixer_agent
```

Make sure Ollama has Llama 3:

```powershell
ollama pull llama3
```

Run the agent:

```powershell
python main.py
```

## Learning Focus

This project intentionally stays Python-only for now. The main learning goal is agentic AI behavior, not multi-language support.

The important concepts are:

- agent loop
- tool use
- short-term memory
- long-term memory
- retry logic
- verification after action
- later, multi-agent coordination
