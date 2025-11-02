class Calendar:
    def __init__(self):
        self.schedule = {}

    def add_event(self, date, event):
        if date not in self.schedule:
            self.schedule[date] = []
        self.schedule[date].append(event)

    def remove_event(self, date, event):
        if date in self.schedule and event in self.schedule[date]:
            self.schedule[date].remove(event)

    def get_events(self, date):
        return self.schedule.get(date, [])

    def display_schedule(self):
        for date, events in sorted(self.schedule.items()):
            print(f"{date}: {', '.join(events)}")