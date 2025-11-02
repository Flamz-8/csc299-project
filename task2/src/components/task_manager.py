class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date=None, priority='normal'):
        task = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'completed': False
        }
        self.tasks.append(task)

    def update_task(self, task_index, title=None, description=None, due_date=None, priority=None):
        if 0 <= task_index < len(self.tasks):
            if title is not None:
                self.tasks[task_index]['title'] = title
            if description is not None:
                self.tasks[task_index]['description'] = description
            if due_date is not None:
                self.tasks[task_index]['due_date'] = due_date
            if priority is not None:
                self.tasks[task_index]['priority'] = priority

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]

    def list_tasks(self):
        return self.tasks

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]['completed'] = True

    def get_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            return self.tasks[task_index]
        return None