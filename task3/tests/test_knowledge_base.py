from tasks3.knowledge_base import KnowledgeBase, Note

def test_note_creation_with_tags():
    kb = KnowledgeBase()
    note_id = kb.add_note(
        title="Python Testing",
        content="Testing is important",
        tags=["python", "testing"]
    )
    note = kb.get_note(note_id)
    assert note.title == "Python Testing"
    assert "python" in note.tags
    assert len(note.tags) == 2

def test_note_search():
    kb = KnowledgeBase()
    kb.add_note(
        title="Search Test",
        content="This is searchable content",
        tags=["search"]
    )
    results = kb.search("searchable")
    assert len(results) == 1
    assert results[0].title == "Search Test"
