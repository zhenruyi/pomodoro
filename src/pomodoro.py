import asyncio
import time

class PomodoroTimer:
    def __init__(self, db):
        self.db = db
        self.running = False

    async def start_pomodoro(self, todo_id, focus_time, break_time, cycles):
        self.running = True
        focus_seconds = focus_time * 60
        break_seconds = break_time * 60
        
        for cycle in range(1, cycles + 1):
            if not self.running:
                break

            print(f"\nCycle {cycle}/{cycles}: Focus for {focus_time} minutes")
            self.db.add_pomodoro(todo_id, focus_time, time.time(), "focus")
            await asyncio.sleep(focus_seconds)
            if not self.running:
                break
            print("Focus session complete")

            # Break
            if cycle < cycles:
                print(f"\nCycle {cycle}/{cycles}: Break for {break_time} minutes")
                self.db.add_pomodoro(todo_id, break_time, time.time(), "break")
                await asyncio.sleep(break_seconds)
                if not self.running:
                    break
                print("Break session complete")

        if self.running:
            print("\nPomodoro session complete")
        self.running = False

    def stop_pomodoro(self):
        self.running = False
        print("Pomodoro session stopped")

        