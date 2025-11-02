import unittest
from src.components.task_manager import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.task_manager = TaskManager()

    def test_add_task(self):
        task = self.task_manager.add_task("Test Task", "This is a test task.")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.body, "This is a test task.")
        self.assertFalse(task.completed)

    def test_update_task(self):
        task = self.task_manager.add_task("Test Task", "This is a test task.")
        updated_task = self.task_manager.update_task(task.id, title="Updated Task", body="Updated body.")
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.body, "Updated body.")

    def test_delete_task(self):
        task = self.task_manager.add_task("Test Task", "This is a test task.")
        self.task_manager.delete_task(task.id)
        with self.assertRaises(KeyError):
            self.task_manager.get_task(task.id)

    def test_complete_task(self):
        task = self.task_manager.add_task("Test Task", "This is a test task.")
        self.task_manager.complete_task(task.id)
        self.assertTrue(task.completed)

if __name__ == '__main__':
    unittest.main()