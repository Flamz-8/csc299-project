import unittest
from src.components.study_tracker import StudyTracker
from src.components.timer import Timer
from src.components.task_manager import TaskManager

class TestStudyTracker(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()
        self.task_manager = TaskManager()
        self.study_tracker = StudyTracker(self.timer, self.task_manager)

    def test_start_study_session(self):
        self.study_tracker.start_study_session()
        self.assertTrue(self.study_tracker.is_studying)

    def test_end_study_session(self):
        self.study_tracker.start_study_session()
        self.study_tracker.end_study_session()
        self.assertFalse(self.study_tracker.is_studying)

    def test_add_task(self):
        self.study_tracker.add_task("Test Task")
        tasks = self.study_tracker.task_manager.get_tasks()
        self.assertIn("Test Task", tasks)

    def test_complete_task(self):
        self.study_tracker.add_task("Test Task")
        self.study_tracker.complete_task("Test Task")
        tasks = self.study_tracker.task_manager.get_tasks()
        self.assertTrue(self.study_tracker.task_manager.is_task_completed("Test Task"))

    def test_timer_functionality(self):
        self.study_tracker.start_study_session()
        self.study_tracker.timer.start(5)  # Start a 5-second timer
        self.assertTrue(self.study_tracker.timer.is_running)

if __name__ == '__main__':
    unittest.main()