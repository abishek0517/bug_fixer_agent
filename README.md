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

Completed:

- Phase 1: First working bug-fixing loop
- Phase 2: Functional better agent loop
- Phase 3: Functional agent memory and history

Next:

- Polish Phase 2 and Phase 3
- Start Phase 4: tool-based agent design

## Current Features

- Runs Python code
- Captures stdout, stderr, and success status
- Sends buggy code and error messages to Ollama
- Uses Llama 3 locally
- Handles missing Ollama responses without crashing
- Retries fixes up to a maximum attempt count
- Saves each attempt in a unique run folder
- Stores run history in `bug_history.json`
- Remembers previous attempts during the current run
- Can fix simple runtime errors and basic logic errors

## Project Structure

```text
Auto Bug Fixer Agent
|
|-- sample_bug.py          Buggy Python input file
|-- runner.py              Runs Python files and captures output
|-- ollama_client.py       Talks to local Ollama
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
