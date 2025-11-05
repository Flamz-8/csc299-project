from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    created_date: datetime
    due_date: Optional[datetime] = None
    completed: bool = False
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str, due_date: Optional[datetime] = None) -> int:
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            created_date=datetime.now(),
            due_date=due_date
        )
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

    def add_tag(self, task_id: int, tag: str) -> bool:
        if task_id in self.tasks:
            if tag not in self.tasks[task_id].tags:
                self.tasks[task_id].tags.append(tag)
            return True
        return False
