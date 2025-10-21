import unittest
from src.components.task_manager import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_add_task(self):
        self.task_manager.add_task("Test Task", "This is a test task.")
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0]['title'], "Test Task")

    def test_list_tasks(self):
        self.task_manager.add_task("Test Task 1", "First test task.")
        self.task_manager.add_task("Test Task 2", "Second test task.")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_complete_task(self):
        self.task_manager.add_task("Test Task", "This task will be completed.")
        self.task_manager.complete_task(0)
        self.assertTrue(self.task_manager.tasks[0]['completed'])

    def test_remove_task(self):
        self.task_manager.add_task("Task to Remove", "This task will be removed.")
        self.task_manager.remove_task(0)
        self.assertEqual(len(self.task_manager.tasks), 0)

if __name__ == '__main__':
    unittest.main()