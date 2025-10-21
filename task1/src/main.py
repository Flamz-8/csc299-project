def main():
    print("Welcome to the Study Planner App!")
    print("Initializing components...")

    # Initialize components
    from components.timer import Timer
    from components.calendar import Calendar
    from components.task_manager import TaskManager

    timer = Timer()
    calendar = Calendar()
    task_manager = TaskManager()

    # Main application loop
    while True:
        print("\nOptions:")
        print("1. Start Timer")
        print("2. Stop Timer")
        print("3. Reset Timer")
        print("4. Show Current Time")
        print("5. Add Event to Calendar")
        print("6. List Tasks")
        print("7. Add Task")
        print("8. Complete Task")
        print("9. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            timer.start()
        elif choice == '2':
            timer.stop()
        elif choice == '3':
            timer.reset()
        elif choice == '4':
            print(f"Current Time: {timer.get_time()}")
        elif choice == '5':
            event = input("Enter event details: ")
            calendar.add_event(event)
        elif choice == '6':
            tasks = task_manager.list_tasks()
            print("Tasks:")
            for task in tasks:
                print(task)
        elif choice == '7':
            task = input("Enter task details: ")
            task_manager.add_task(task)
        elif choice == '8':
            task_id = input("Enter task ID to complete: ")
            task_manager.complete_task(task_id)
        elif choice == '9':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()