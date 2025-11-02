class Task:
    def __init__(self, id, title, description, due_date, priority, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed

class Note:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

class StudySession:
    def __init__(self, id, task_id, start_time, end_time):
        self.id = id
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = end_time