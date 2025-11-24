To create this project I went through 3 different repositories. The first one I just screwed up creating it so I had to restart. The second one I had created something alot more complicated than needed for this project. And the third one where I was finally able to tell the speckit exactly what I wanted. 
For the project constitution I used the given template to fill in the blanks. I went in afterward and asked it to make sure users had documentation and were up to date. For the specification prompt, I created a detailed prompt with the help of ChatGPT. "create a prompt for speckit.specify for a pkms app that helps students track their notes and tasks, making it easier for students to keep track of their todos". This what I asked. And this is what it returned: 

"/speckit.specify Build a terminal-based personal knowledge management (PKM) app for students that helps them capture class notes and manage tasks/todos in one place. It does not need a GUI; everything should run in a standard terminal for Linux/macOS/Windows with minimal setup.
Primary users: high school and college students juggling multiple classes, assignments, and exams.
Requirements:
Run entirely in the terminal (CLI only), using simple text menus or commands.
Allow students to:
Create, edit, and organize notes by course and topic.
Create tasks/todos with due dates, optional priority, and optional subtasks.
Link notes to tasks (e.g., a task can reference one or more note entries).
View filtered lists of tasks:
Today
This week
Overdue
All by course
Quickly add “inbox” notes or tasks with minimal fields, to organize later.
Search notes and tasks by keyword, course, or tag.
Provide a simple onboarding/help command that lists the main commands and keybindings.
Store data locally in human-readable files (e.g., JSON or plain text) so users don’t need a database.Require no external services or accounts; everything is offline and local.
Core goals: Reduce cognitive load by keeping notes and todos together in a lightweight, fast CLI tool. Make it obvious what to work on next using simple lists and due date views. Be easy enough that stressed students will actually use it daily (few commands, low friction). Non-goals:No graphical UI or web interface.No complex collaboration; single-user only.No advanced analytics; focus on straightforward capture, organization, and review."

After I plugged in this prompt, I used /speckit.clarify have Claude read through to make sure it didn't miss anything important. 
Claude created a new folder called specs where it would create the specifications and intstructions for the ai to follow when it finally implements the instructions. 