class Timer:
    def __init__(self):
        self.time_left = 0
        self.is_running = False

    def start(self, duration):
        """Start the timer with a specified duration in seconds."""
        self.time_left = duration
        self.is_running = True

    def tick(self):
        """Decrement the timer by one second if it's running."""
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            if self.time_left == 0:
                self.is_running = False

    def get_time_left(self):
        """Return the time left in seconds."""
        return self.time_left

    def stop(self):
        """Stop the timer."""
        self.is_running = False

    def reset(self):
        """Reset the timer to zero."""
        self.time_left = 0
        self.is_running = False