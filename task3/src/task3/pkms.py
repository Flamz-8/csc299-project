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
        os.makedirs(self.data_dir, exist_ok=True)  # Just create directory if needed
        self._load_data()

    def _clear_data_dir(self) -> None:
        """Clear all data files in the data directory"""
        if os.path.exists(self.data_dir):
            tasks_file = os.path.join(self.data_dir, "tasks.json")
            notes_file = os.path.join(self.data_dir, "notes.json")
            if os.path.exists(tasks_file):
                os.remove(tasks_file)
            if os.path.exists(notes_file):
                os.remove(notes_file)

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

    def _load_tasks(self) -> None:
        tasks_file = os.path.join(self.data_dir, "tasks.json")
        if os.path.exists(tasks_file):
            try:
                with open(tasks_file, 'r') as f:
                    data = json.load(f)
                    for task_dict in data.get('tasks', []):
                        task_dict['created_date'] = datetime.fromisoformat(task_dict['created_date'])
                        task_dict['related_notes'] = set(task_dict['related_notes'])
                        self.tasks[task_dict['id']] = Task(**task_dict)
                    self.next_task_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading tasks: {e}")
                self.tasks = {}
                self.next_task_id = 1

    def _save_tasks(self) -> None:
        tasks_file = os.path.join(self.data_dir, "tasks.json")
        try:
            tasks_data = []
            for task in self.tasks.values():
                task_dict = asdict(task)
                task_dict['created_date'] = task_dict['created_date'].isoformat()
                task_dict['related_notes'] = list(task_dict['related_notes'])
                tasks_data.append(task_dict)
            
            with open(tasks_file, 'w') as f:
                json.dump({
                    'tasks': tasks_data,
                    'next_id': self.next_task_id
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def _load_notes(self) -> None:
        notes_file = os.path.join(self.data_dir, "notes.json")
        if os.path.exists(notes_file):
            try:
                with open(notes_file, 'r') as f:
                    data = json.load(f)
                    for note_dict in data.get('notes', []):
                        note_dict['created_date'] = datetime.fromisoformat(note_dict['created_date'])
                        note_dict['related_tasks'] = set(note_dict['related_tasks'])
                        self.notes[note_dict['id']] = Note(**note_dict)
                    self.next_note_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading notes: {e}")
                self.notes = {}
                self.next_note_id = 1

    def _save_notes(self) -> None:
        notes_file = os.path.join(self.data_dir, "notes.json")
        try:
            notes_data = []
            for note in self.notes.values():
                note_dict = asdict(note)
                note_dict['created_date'] = note_dict['created_date'].isoformat()
                note_dict['related_tasks'] = list(note_dict['related_tasks'])
                notes_data.append(note_dict)
            
            with open(notes_file, 'w') as f:
                json.dump({
                    'notes': notes_data,
                    'next_id': self.next_note_id
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving notes: {e}")

    def reset(self) -> None:
        """Reset the PKMS to initial state"""
        self._clear_data_dir()  # Clear files first
        self.tasks.clear()
        self.notes.clear()
        self.next_task_id = 1
        self.next_note_id = 1
        self._save_data()  # Save empty state
