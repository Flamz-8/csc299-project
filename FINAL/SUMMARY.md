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

After I plugged in this prompt, Claude created a new folder called specs where it would create the specifications and intstructions for the ai to follow when it finally implements the instructions. I wanted it to list tasks by urgency and closest due date so I put "list tasks by urgency and due dates" into Claude. Once I couldn't think of anything else to add I used /speckit.clarify to see if Claude had any last minute features to add which it didn't. 
Once I was done with that I started creating the plan with /speckit.plan. I added that I wanted Claude to use python to create and 'uv' to initialize the project since it's what we worked with in class. This created a new plan.md file in which it layed out the plan and project structure. After that I took decided to have Claude create AUDIT.md in which it analyzed all the documentation to make sure I'm finally ready to impliment, it warned me about not having a tasks.md file. So to create it I used /speckit.tasks. This file designates the creation of the project into 11 phases in which phase (3-10) works through the 7 user stories. These stories are basically just the different features this app would provide. 
Once I was ready I finally implemented it with /speckit.implement. Some last minute changes I made were changing the name of the app from the default the ai created to Pro Study Planner. Once it was fully implemented I also tried to make the ID's a little more user friendly. 