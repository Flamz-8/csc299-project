from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    created_date: datetime = datetime.now()
    completed: bool = False

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title: str, description: str) -> int:
        task = Task(id=self.next_id, title=title, description=description)
        self.tasks[task.id] = task
        self.next_id += 1
        return task.id

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def mark_complete(self, task_id: int) -> bool:
        if task_id in self.tasks:
            self.tasks[task_id].completed = True
            return True
        return False
