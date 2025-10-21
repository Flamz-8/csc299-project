class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date):
        task = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'completed': False
        }
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index]['completed'] = True
        else:
            raise IndexError("Task index out of range")