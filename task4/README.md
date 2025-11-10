# task4 — Paragraph Summarizer

Overview
- Sends paragraph-length task descriptions to the OpenAI Chat Completions API (model gpt-5-mini) and prints concise phrase summaries for each paragraph.

Prerequisites
- Python 3.11 (see `.python-version`)
- OpenAI API key (do not commit this key)
- Install dependency: `pip install openai`
- Optional: `pip install python-dotenv` (if you want to load a `.env` file)

Setup
- Create and activate a virtual environment:
  - Windows (PowerShell):
    - `python -m venv .venv`
    - `.\.venv\Scripts\Activate.ps1`
  - macOS / Linux:
    - `python -m venv .venv`
    - `source .venv/bin/activate`
- Using uv (recommended):
  - `uv add openai`
  - Optional: `uv add python-dotenv`
- Or with pip:
  - `pip install openai`
  - Optional: `pip install python-dotenv`

Set the OPENAI_API_KEY
- macOS / Linux (current shell):
  - `export OPENAI_API_KEY="sk-..."`
- Windows PowerShell (current session):
  - `$env:OPENAI_API_KEY="sk-..."`
- Persist on Windows (PowerShell):
  - `[Environment]::SetEnvironmentVariable("OPENAI_API_KEY","sk-...","User")` (restart terminal)
- Using a `.env` file (optional for local dev):
  - Create `.env` with: `OPENAI_API_KEY=sk-...`
  - In code, load it early:
    - `from dotenv import load_dotenv; load_dotenv()`

Run
- From the repo root:
  - `python -m task4`
- Or run the module file directly:
  - `python src/task4/__init__.py`
- With uv (optional):
  - `uv run python -m task4`
  - `uv run task4` (after adding dependencies with `uv add openai`)
  - If you see "Missing dependency 'openai'..." install the package as above.

Expected output
- The script iterates sample paragraphs and prints short-phrase summaries, e.g.:
  - `Summary 1: Large-files-report`
  - `Summary 2: CSV-stats-service`
  - `Summary 3: Test-harness`

Notes
- Do not hardcode or commit API keys. Add `.env` to `.gitignore`.
- The program raises an error if `OPENAI_API_KEY` is not set.
- API/network errors may appear in output as `<error: ...>`.
- If openai is not installed the program prints an instruction and exits.
- Uninstall warning ("missing RECORD" in task4-0.1.0.dist-info) fix:
  1. Deactivate the virtual environment.
  2. Remove the broken folder: `.venv/Lib/site-packages/task4-0.1.0.dist-info`
  3. Reinstall the project package (if you have packaging config): `uv add .` or `pip install -e .`
  4. Ensure a proper `pyproject.toml` exists; incomplete installs cause missing RECORD.
