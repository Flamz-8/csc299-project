class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, title, date, time):
        event = {
            'title': title,
            'date': date,
            'time': time
        }
        self.events.append(event)

    def display_events(self):
        if not self.events:
            return "No events scheduled."
        return "\n".join(f"{event['title']} on {event['date']} at {event['time']}" for event in self.events)

    def clear_events(self):
        self.events = []