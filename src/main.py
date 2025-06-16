# import asyncio
# import platform
# from src.pomodoro import PomodoroTimer
# from src.todo import TodoManager
# from src.database import Database
# from src.analytics import Analytics
#
# async def main():
#     db = Database()
#     db.initialize()
#
#     todo_manager = TodoManager(db)
#     pomodoro_timer = PomodoroTimer(db)
#     analytics = Analytics(db)
#
#     while True:
#         print("\nPomodoro Todo App")
#         print("1. Add Todo")
#         print("2. List Todos")
#         print("3. Start Pomodoro for Todo")
#         print("4. View Analytics")
#         print("5. Exit")
#         choice = input("Enter your choice: ")
#
#         if choice == '1':
#             title = input("Enter todo title: ")
#             content = input("Enter todo content: ")
#             is_periodic = input("Is this todo periodic? (daily/weekly/none): ").lower()
#             period = is_periodic if is_periodic in ["daily", "weekly"] else "none"
#             todo_manager.add_todo(title, content, period)
#             print(f"Added todo: {title}")
#
#         elif choice == '2':
#             todos = todo_manager.list_todos()
#             for todo in todos:
#                 period = todo[3] if todo[3] != "none" else "once"
#                 print(f"ID: {todo[0]}, Title: {todo[1]}, Content: {todo[2]}, Period: {period}")
#
#         elif choice == '3':
#             todo_id = input("Enter todo ID: ")
#             try:
#                 todo_id = int(todo_id)
#                 focus_time = int(input("Enter focus time (in minutes): ") or 25)
#                 break_time = int(input("Enter break time (in minutes): ") or 5)
#                 cycles = int(input("Enter number of cycles: ") or 4)
#                 await pomodoro_timer.start_pomodoro(todo_id, focus_time, break_time, cycles)
#             except ValueError:
#                 print("Invalid input. Please enter numbers.")
#
#         elif choice == '4':
#             analytics.generate_report()
#
#         elif choice == '5':
#             print("Exiting...")
#             break
#
#         else:
#             print("Invalid choice. Please try again.")
#
# if __name__ == "__main__":
#     asyncio.run(main())


import tkinter as tk
from src.pomodoro import PomodoroTimer
from src.todo import TodoManager
from src.database import Database
from src.analytics import Analytics
from src.gui import PomodoroGUI


def main():
    # 初始化数据库
    db = Database()
    db.initialize()

    # 初始化管理器
    todo_manager = TodoManager(db)
    pomodoro_timer = PomodoroTimer(db)
    analytics = Analytics(db)

    # 初始化 GUI
    root = tk.Tk()
    app = PomodoroGUI(root, todo_manager, pomodoro_timer, analytics)
    root.mainloop()

    # 关闭数据库
    db.close()


if __name__ == "__main__":
    main()