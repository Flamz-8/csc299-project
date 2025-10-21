import unittest
from src.components.timer import Timer

class TestTimer(unittest.TestCase):

    def setUp(self):
        self.timer = Timer()

    def test_initial_time(self):
        self.assertEqual(self.timer.get_time(), 0)

    def test_start_timer(self):
        self.timer.start()
        self.assertTrue(self.timer.running)

    def test_stop_timer(self):
        self.timer.start()
        self.timer.stop()
        self.assertFalse(self.timer.running)

    def test_reset_timer(self):
        self.timer.start()
        self.timer.reset()
        self.assertEqual(self.timer.get_time(), 0)

    def test_timer_running_state(self):
        self.timer.start()
        self.timer.stop()
        self.timer.start()
        self.assertTrue(self.timer.running)

if __name__ == '__main__':
    unittest.main()