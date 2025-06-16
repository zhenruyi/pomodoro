from collections import defaultdict
import time

class Analytics:
    def __init__(self, db):
        self.db = db

    def generate_report(self):
        pomodoros = self.db.get_pomodoros()
        if not pomodoros:
            print("No pomodoros recorded")
            return

        total_focus_time = 0
        todo_focus_time = defaultdict(int)
        daily_focus_time = defaultdict(int)

        for todo_id, duration, start_time, session_type in pomodoros:
            if session_type == "focus":
                total_focus_time += duration
                todo_focus_time[todo_id] += duration
                day = time.strftime("%Y-%m-%d", time.localtime(start_time))
                daily_focus_time[day] += duration

        print("\nPomodoro Analytics Report")
        print("------------------------")
        print(f"Total Focus Time: {total_focus_time // 60} minutes")

        print("\nFocus Time by Todo:")
        todos = self.db.get_todos()
        todo_dict = {todo[0]: todo[1] for todo in todos}
        for todo_id, focus_time in todo_focus_time.items():
            title = todo_dict.get(todo_id, "Unknown")
            print(f"Todo '{title}' (ID: {todo_id}): {focus_time // 60} minutes")

        print("\nFocus Time by Day:")
        for day, focus_time in sorted(daily_focus_time.items()):
            print(f"{day}: {focus_time // 60} minutes")