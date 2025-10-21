class Timer:
    def __init__(self):
        self.time = 0
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            # Logic to start the timer
            print("Timer started.")

    def stop(self):
        if self.running:
            self.running = False
            # Logic to stop the timer
            print("Timer stopped.")

    def reset(self):
        self.time = 0
        if self.running:
            # Logic to reset the timer while running
            print("Timer reset while running.")
        print("Timer reset.")

    def get_time(self):
        return self.time

    def update(self):
        if self.running:
            # Logic to update the timer
            print("Timer updated.")