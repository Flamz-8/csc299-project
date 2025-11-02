class StudyTracker:
    def __init__(self, timer, task_manager):
        self.timer = timer
        self.task_manager = task_manager
        self.study_sessions = []

    def start_study_session(self, task_title):
        task = self.task_manager.get_task(task_title)
        if task:
            self.timer.start()
            self.study_sessions.append(task)
            print(f"Started studying: {task.title}")
        else:
            print("Task not found.")

    def end_study_session(self):
        elapsed_time = self.timer.stop()
        if self.study_sessions:
            task = self.study_sessions.pop()
            task.add_time(elapsed_time)
            print(f"Ended studying: {task.title}. Time spent: {elapsed_time} seconds.")
        else:
            print("No active study session.")

    def get_study_progress(self):
        progress = {}
        for task in self.study_sessions:
            progress[task.title] = task.get_time_spent()
        return progress

    def display_progress(self):
        progress = self.get_study_progress()
        for title, time_spent in progress.items():
            print(f"Task: {title}, Time Spent: {time_spent} seconds")