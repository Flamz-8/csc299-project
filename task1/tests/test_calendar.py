import unittest
from src.components.calendar import Calendar

class TestCalendar(unittest.TestCase):

    def setUp(self):
        self.calendar = Calendar()

    def test_add_event(self):
        self.calendar.add_event("2023-10-01", "Meeting")
        events = self.calendar.get_events("2023-10-01")
        self.assertIn("Meeting", events)

    def test_get_events_empty(self):
        events = self.calendar.get_events("2023-10-02")
        self.assertEqual(events, [])

    def test_display_calendar(self):
        self.calendar.add_event("2023-10-01", "Meeting")
        output = self.calendar.display_calendar("2023-10")
        self.assertIn("Meeting", output)

if __name__ == '__main__':
    unittest.main()