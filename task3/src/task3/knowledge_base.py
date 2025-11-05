from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class Note:
    title: str
    content: str
    tags: List[str] = field(default_factory=list)

class KnowledgeBase:
    def __init__(self):
        self.notes: Dict[int, Note] = {}
        self.next_id: int = 1

    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> int:
        note = Note(title=title, content=content, tags=tags or [])
        self.notes[self.next_id] = note
        self.next_id += 1
        return self.next_id - 1

    def get_note(self, note_id: int) -> Optional[Note]:
        return self.notes.get(note_id)

    def search(self, query: str) -> List[Note]:
        return [note for note in self.notes.values() 
                if query.lower() in note.title.lower()]
