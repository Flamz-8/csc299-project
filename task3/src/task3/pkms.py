import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional, List, Dict, Set

@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: str
    tags: List[str]
    category: str
    related_notes: Set[int] = field(default_factory=set)
    created_date: datetime = field(default_factory=datetime.now)
    completed: bool = False

@dataclass
class Note:
    id: int
    title: str
    content: str
    tags: List[str]
    related_tasks: Set[int] = field(default_factory=set)
    created_date: datetime = field(default_factory=datetime.now)

class PKMS:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.notes: Dict[int, Note] = {}
        self.next_task_id = 1
        self.next_note_id = 1
        self.data_dir = os.path.expanduser("~/.task3")
        self._load_data()

    def add_task(self, title: str, description: str, priority: str = "Medium", 
                tags: List[str] = None, category: str = "General") -> int:
        task = Task(
            id=self.next_task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            category=category
        )
        self.tasks[task.id] = task
        self.next_task_id += 1
        self._save_data()
        return task.id

    def add_note(self, title: str, content: str, tags: List[str] = None) -> int:
        note = Note(
            id=self.next_note_id,
            title=title,
            content=content,
            tags=tags or []
        )
        self.notes[note.id] = note
        self.next_note_id += 1
        self._save_data()
        return note.id

    def link_task_note(self, task_id: int, note_id: int) -> bool:
        if task_id in self.tasks and note_id in self.notes:
            self.tasks[task_id].related_notes.add(note_id)
            self.notes[note_id].related_tasks.add(task_id)
            self._save_data()
            return True
        return False

    def search(self, query: str) -> tuple[List[Task], List[Note]]:
        """Search both tasks and notes"""
        query = query.lower()
        tasks = [
            task for task in self.tasks.values()
            if query in task.title.lower() or
               query in task.description.lower() or
               any(query in tag.lower() for tag in task.tags)
        ]
        notes = [
            note for note in self.notes.values()
            if query in note.title.lower() or
               query in note.content.lower() or
               any(query in tag.lower() for tag in note.tags)
        ]
        return tasks, notes

    def _load_data(self) -> None:
        os.makedirs(self.data_dir, exist_ok=True)
        self._load_tasks()
        self._load_notes()

    def _save_data(self) -> None:
        self._save_tasks()
        self._save_notes()

    # ... Add _load_tasks, _save_tasks, _load_notes, _save_notes methods similar to original implementation
