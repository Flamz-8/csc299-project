StudyMate — Project Plan

Overview

StudyMate is an AI-powered terminal Personal Knowledge Management System (PKMS) and task manager for students. It stores notes and tasks in SQLite, provides a chat-style terminal interface, and includes AI agents for summarization and flashcard generation. The system exports/imports JSON and has tests for key components.

Project Contract (tiny)

- Inputs: terminal chat commands and optional file imports (JSON/TXT).
- Outputs: SQLite database and AI-generated summaries/flashcards shown in the terminal.
- Error modes: DB migration issues, invalid commands, missing OpenAI API key.
- Success criteria: Add/read/update/delete notes and tasks; summarize notes; generate flashcards; export/import JSON.

MVP Features

- SQLite DB with notes, tasks, tags, note_tags, task_tags, links, settings.
- Terminal REPL accepting commands such as add/list/show/summarize/generate quiz/complete/export/import.
- AI summarizer and quiz generator using OpenAI (with fallback summarizer).
- JSON export/import and a sample dataset.
- Unit tests for DB and command parser.

Data Schema (SQLite)

Tables

- notes(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, body TEXT, created_ts DATETIME DEFAULT CURRENT_TIMESTAMP, updated_ts DATETIME)
- tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, body TEXT, due DATE, priority TEXT, completed INTEGER DEFAULT 0, created_ts DATETIME DEFAULT CURRENT_TIMESTAMP, updated_ts DATETIME)
- tags(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)
- note_tags(note_id INTEGER, tag_id INTEGER, PRIMARY KEY(note_id, tag_id))
- task_tags(task_id INTEGER, tag_id INTEGER, PRIMARY KEY(task_id, tag_id))
- links(id INTEGER PRIMARY KEY AUTOINCREMENT, from_note_id INTEGER, to_note_id INTEGER, description TEXT)
- settings(key TEXT PRIMARY KEY, value TEXT)

File Structure

- README.md  — project overview and quick start
- PROJECT_PLAN.md — this file
- requirements.txt — dependencies (prompt_toolkit, rich, openai, pytest)
- studyme/
  - __main__.py — module entrypoint (python -m studyme)
  - app.py — app runner and orchestration
  - db.py — SQLite connection, migrations, helpers
  - models.py — DB CRUD wrappers for notes/tasks/tags
  - commands.py — parse and dispatch chat commands
  - agents.py — Summarizer and Quiz generators
  - ui.py — prompt loop using prompt_toolkit or simple input()
  - config.py — load/save settings.json
  - export.py — import/export JSON
  - tests/ — pytest tests for DB and commands
- sample_data/export.json — sample exported data
- video.txt — demo script

CLI Commands (examples)

- add note "TITLE" body:"Long text..." tags:tag1,tag2
- list notes [tag:calculus]
- show note 3
- summarize note 3
- generate quiz note 3
- add task "TITLE" due:YYYY-MM-DD priority:high tags:cs101
- list tasks due:7d tag:cs101
- complete task 5
- export json path
- import json path
- help

Command parsing notes

- Use a small lexer to capture quoted strings and key:value pairs.
- Map parsed command and args to handlers in `commands.py`.

AI Agents

- SummarizerAgent:
  - Use OpenAI completions if OPENAI_API_KEY configured.
  - Fallback: extractive summarizer (rank sentences by TF-IDF) when no key is present.
- QuizAgent:
  - Generate 4-6 flashcards (question/answer pairs) from note text.
  - Use LLM if available; otherwise use sentence-to-question templates.

Testing

- Use pytest.
- DB tests: create in-memory SQLite DB and test note/task CRUD.
- Parser tests: assert correct parse of example commands.
- Agent tests: mock OpenAI responses and test fallback behaviour.

Milestones

1. DB schema and migrations
2. DB layer and models (CRUD)
3. CLI parser and REPL UI
4. AI agent integration (OpenAI + fallback)
5. Search, linking, tags
6. Export/import and sample data
7. Tests and linting
8. README, video.txt and final polish

Video script outline (video.txt)

0:00–0:30 — Title + one-liner on value
0:30–1:00 — Architecture: Python, SQLite, CLI, AI agents
1:00–3:00 — Live demo: create note, summarize, generate quiz, add task, list tasks
3:00–4:00 — Show DB or JSON export
4:00–5:00 — Discuss AI integration and fallback
5:00–6:00 — Challenges learned and next steps

How I can help next

- Scaffold the project and implement the MVP now (create files, DB, CLI, summarizer). 
- Or produce detailed code snippets for each file for you to paste and run.

Choose which and I will proceed. If you want the scaffold, I'll start creating files and implementing the DB layer next.