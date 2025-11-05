import pytest
from task3.knowledge_base import KnowledgeBase

def test_note_creation_and_retrieval():
    kb = KnowledgeBase()
    note_id = kb.add_note(
        "Test Note",
        "Test content",
        tags=["test", "example"]
    )
    note = kb.get_note(note_id)
    
    assert note.title == "Test Note"
    assert note.content == "Test content"
    assert "test" in note.tags
    assert len(note.tags) == 2

def test_note_search():
    kb = KnowledgeBase()
    kb.add_note("Python Note", "Python is great", ["python"])
    kb.add_note("Other Note", "Something else", ["other"])
    
    results = kb.search("python")
    assert len(results) == 1
    assert results[0].title == "Python Note"
