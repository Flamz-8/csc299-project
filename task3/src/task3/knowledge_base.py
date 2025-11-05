from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class Note:
    id: int
    title: str
    content: str
    created_date: datetime
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class KnowledgeBase:
    def __init__(self):
        self.notes: Dict[int, Note] = {}
        self.next_id: int = 1

    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> int:
        note = Note(
            id=self.next_id,
            title=title,
            content=content,
            created_date=datetime.now(),
            tags=tags or []
        )
        self.notes[note.id] = note
        self.next_id += 1
        return note.id

    def get_note(self, note_id: int) -> Optional[Note]:
        return self.notes.get(note_id)

    def search(self, query: str) -> List[Note]:
        results = []
        query = query.lower()
        for note in self.notes.values():
            if (query in note.title.lower() or 
                query in note.content.lower() or 
                any(query in tag.lower() for tag in note.tags)):
                results.append(note)
        return results
