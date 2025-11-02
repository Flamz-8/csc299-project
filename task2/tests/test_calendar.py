import unittest
from src.components.calendar import Calendar

class TestCalendar(unittest.TestCase):

    def setUp(self):
        self.calendar = Calendar()

    def test_add_event(self):
        self.calendar.add_event("2023-10-01", "Study Python")
        events = self.calendar.get_events("2023-10-01")
        self.assertIn("Study Python", events)

    def test_remove_event(self):
        self.calendar.add_event("2023-10-01", "Study Python")
        self.calendar.remove_event("2023-10-01", "Study Python")
        events = self.calendar.get_events("2023-10-01")
        self.assertNotIn("Study Python", events)

    def test_get_events(self):
        self.calendar.add_event("2023-10-01", "Study Python")
        self.calendar.add_event("2023-10-01", "Study Math")
        events = self.calendar.get_events("2023-10-01")
        self.assertEqual(len(events), 2)

    def test_schedule_conflict(self):
        self.calendar.add_event("2023-10-01", "Study Python")
        with self.assertRaises(ValueError):
            self.calendar.add_event("2023-10-01", "Study Python")  # Conflict

if __name__ == '__main__':
    unittest.main()