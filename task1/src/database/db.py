class Database:
    def __init__(self, db_name='task_manager.db'):
        import sqlite3
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.connection.commit()

    def add_task(self, title, description, due_date):
        self.cursor.execute('''
            INSERT INTO tasks (title, description, due_date)
            VALUES (?, ?, ?)
        ''', (title, description, due_date))
        self.connection.commit()

    def get_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        return self.cursor.fetchall()

    def complete_task(self, task_id):
        self.cursor.execute('''
            UPDATE tasks SET completed = 1 WHERE id = ?
        ''', (task_id,))
        self.connection.commit()

    def add_event(self, title, date, description):
        self.cursor.execute('''
            INSERT INTO events (title, date, description)
            VALUES (?, ?, ?)
        ''', (title, date, description))
        self.connection.commit()

    def get_events(self):
        self.cursor.execute('SELECT * FROM events')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()