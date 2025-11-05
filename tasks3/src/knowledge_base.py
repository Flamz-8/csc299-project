class KnowledgeBase:
    """KnowledgeBase manages a collection of notes with search capability.
    
    Provides methods for creating, retrieving, and searching notes
    with support for tagging.
    """
    
    def __init__(self):
        """Initialize an empty knowledge base."""
        self.notes = []
        self.next_id = 1

    def add_note(self, title: str, content: str, tags: Optional[List[str]] = None) -> int:
        """Create a new note and return its ID.
        
        Args:
            title: The note title
            content: The note content
            tags: Optional list of tags to categorize the note
            
        Returns:
            int: The ID of the created note
        """
        note = Note(id=self.next_id, title=title, content=content, tags=tags or [])
        self.notes.append(note)
        self.next_id += 1
        return note.id

    def search(self, query: str) -> List[Note]:
        """Search notes by title, content, or tags.
        
        Args:
            query: Search string to match against notes
            
        Returns:
            List[Note]: List of notes matching the search query
        """
        query = query.lower()
        return [note for note in self.notes if 
                query in note.title.lower() or 
                query in note.content.lower() or 
                any(query in tag.lower() for tag in note.tags)]