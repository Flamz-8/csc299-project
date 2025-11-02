def main():
    print("Welcome to Task2: Your Study Planner App!")
    print("Available commands:")
    print("1. start_timer - Start a study session timer")
    print("2. add_task - Add a new task")
    print("3. view_tasks - View all tasks")
    print("4. schedule - Schedule a study session")
    print("5. exit - Exit the application")

    while True:
        command = input("Enter a command: ").strip().lower()
        
        if command == "start_timer":
            # Logic to start the timer
            pass
        elif command == "add_task":
            # Logic to add a task
            pass
        elif command == "view_tasks":
            # Logic to view tasks
            pass
        elif command == "schedule":
            # Logic to schedule a study session
            pass
        elif command == "exit":
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()