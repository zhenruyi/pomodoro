import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import time

class PomodoroGUI:
    def __init__(self, root, todo_manager, pomodoro_timer, analytics):
        self.root = root
        self.todo_manager = todo_manager
        self.pomodoro_timer = pomodoro_timer
        self.analytics = analytics
        self.running = False
        self.current_cycle = 0
        self.total_cycles = 0
        self.current_phase = ""
        self.remaining_time = 0
        self.root.title("番茄待办应用")
        self.setup_gui()

    def setup_gui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 待办事项输入区域
        ttk.Label(main_frame, text="标题:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(main_frame, width=30)
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="内容:").grid(row=1, column=0, sticky=tk.W)
        self.content_entry = ttk.Entry(main_frame, width=30)
        self.content_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(main_frame, text="周期性:").grid(row=2, column=0, sticky=tk.W)
        self.period_var = tk.StringVar(value="none")
        period_options = ["none", "daily", "weekly"]
        self.period_menu = ttk.OptionMenu(main_frame, self.period_var, "none", *period_options)
        self.period_menu.grid(row=2, column=1, sticky=(tk.W, tk.E))

        ttk.Button(main_frame, text="添加待办", command=self.add_todo).grid(row=2, column=2, sticky=tk.E)

        # 待办事项列表
        self.todo_listbox = tk.Listbox(main_frame, width=50, height=10)
        self.todo_listbox.grid(row=3, column=0, columnspan=3, pady=10)
        self.update_todo_list()

        # 番茄时钟设置
        ttk.Label(main_frame, text="专注时长 (分钟):").grid(row=4, column=0, sticky=tk.W)
        self.focus_entry = ttk.Entry(main_frame, width=10)
        self.focus_entry.insert(0, "25")
        self.focus_entry.grid(row=4, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="休息时长 (分钟):").grid(row=5, column=0, sticky=tk.W)
        self.break_entry = ttk.Entry(main_frame, width=10)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=5, column=1, sticky=tk.W)

        ttk.Label(main_frame, text="循环次数:").grid(row=6, column=0, sticky=tk.W)
        self.cycles_entry = ttk.Entry(main_frame, width=10)
        self.cycles_entry.insert(0, "4")
        self.cycles_entry.grid(row=6, column=1, sticky=tk.W)

        self.start_button = ttk.Button(main_frame, text="启动番茄", command=self.start_pomodoro)
        self.start_button.grid(row=6, column=2, sticky=tk.E)

        # 计时显示
        self.timer_label = ttk.Label(main_frame, text="未开始", font=("Arial", 14))
        self.timer_label.grid(row=7, column=0, columnspan=3, pady=10)

        # 统计报告
        ttk.Button(main_frame, text="查看统计", command=self.show_analytics).grid(row=8, column=0, columnspan=3)
        self.analytics_text = tk.Text(main_frame, width=50, height=10)
        self.analytics_text.grid(row=9, column=0, columnspan=3, pady=10)

    def add_todo(self):
        title = self.title_entry.get()
        content = self.content_entry.get()
        period = self.period_var.get()
        if not title:
            messagebox.showerror("错误", "标题不能为空！")
            return
        self.todo_manager.add_todo(title, content, period)
        self.update_todo_list()
        self.title_entry.delete(0, tk.END)
        self.content_entry.delete(0, tk.END)
        self.period_var.set("none")
        messagebox.showinfo("成功", "待办事项已添加！")

    def update_todo_list(self):
        self.todo_listbox.delete(0, tk.END)
        todos = self.todo_manager.list_todos()
        for todo in todos:
            period = todo[3] if todo[3] != "none" else "一次性"
            self.todo_listbox.insert(tk.END, f"ID: {todo[0]} | {todo[1]} | {todo[2]} | {period}")

    def start_pomodoro(self):
        if self.running:
            self.pomodoro_timer.stop_pomodoro()
            self.start_button.configure(text="启动番茄")
            self.running = False
            self.timer_label.configure(text="已暂停")
            self.root.after_cancel(self.timer_update_id)
            return

        try:
            selection = self.todo_listbox.curselection()
            if not selection:
                messagebox.showerror("错误", "请先选择一个待办事项！")
                return
            todo_id = int(self.todo_listbox.get(selection[0]).split("|")[0].split(":")[1].strip())
            focus_time = int(self.focus_entry.get() or 25)
            break_time = int(self.break_entry.get() or 5)
            cycles = int(self.cycles_entry.get() or 4)
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")
            return

        self.running = True
        self.start_button.configure(text="暂停番茄")
        self.current_cycle = 1
        self.total_cycles = cycles
        self.current_phase = "focus"
        self.remaining_time = focus_time * 60
        self.pomodoro_params = (todo_id, focus_time, break_time, cycles)
        self.start_pomodoro_session()

    def start_pomodoro_session(self):
        self.update_timer_label()
        self.timer_update_id = self.root.after(1000, self.update_timer)
        asyncio.run_coroutine_threadsafe(self.run_pomodoro(), asyncio.get_event_loop())

    def update_timer(self):
        if not self.running:
            return
        self.remaining_time -= 1
        self.update_timer_label()
        if self.remaining_time > 0:
            self.timer_update_id = self.root.after(1000, self.update_timer)
        else:
            self.advance_pomodoro()

    def update_timer_label(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.configure(text=f"第 {self.current_cycle}/{self.total_cycles} 轮：{self.current_phase} {minutes:02d}:{seconds:02d}")

    def advance_pomodoro(self):
        todo_id, focus_time, break_time, cycles = self.pomodoro_params
        if self.current_phase == "focus":
            self.db.add_pomodoro_session(todo_id, focus_time, time.time() - focus_time * 60, "focus")
            if self.current_cycle < cycles:
                self.current_phase = "break"
                self.remaining_time = break_time * 60
                self.update_timer_label()
                self.timer_update_id = self.root.after(1000, self.update_timer)
            else:
                self.finish_pomodoro()
        else:  # break
            self.db.add_pomodoro_session(todo_id, break_time, time.time() - break_time * 60, "break")
            self.current_cycle += 1
            if self.current_cycle <= cycles:
                self.current_phase = "focus"
                self.remaining_time = focus_time * 60
                self.update_timer_label()
                self.timer_update_id = self.root.after(1000, self.update_timer)
            else:
                self.finish_pomodoro()

    def finish_pomodoro(self):
        self.running = False
        self.start_button.configure(text="启动番茄")
        self.timer_label.configure(text="番茄时钟完成！")
        self.root.event_generate("<<PomodoroDone>>", when="tail")

    async def run_pomodoro(self):
        todo_id, focus_time, break_time, cycles = self.pomodoro_params
        await self.pomodoro_timer.start_pomodoro(todo_id, focus_time, break_time, cycles)

    def show_analytics(self):
        self.analytics_text.delete(1.0, tk.END)
        sessions = self.pomodoro_timer.db.get_pomodoros()
        if not sessions:
            self.analytics_text.insert(tk.END, "暂无番茄时钟记录。\n")
            return

        total_focus_time = 0
        todo_focus_time = {}
        daily_focus_time = {}
        todos = self.todo_manager.list_todos()
        todo_dict = {todo[0]: todo[1] for todo in todos}

        for todo_id, duration, start_time, session_type in sessions:
            if session_type == "focus":
                total_focus_time += duration
                todo_focus_time[todo_id] = todo_focus_time.get(todo_id, 0) + duration
                day = time.strftime("%Y-%m-%d", time.localtime(start_time))
                daily_focus_time[day] = daily_focus_time.get(day, 0) + duration

        report = "番茄时钟统计报告\n" + "-"*20 + "\n"
        report += f"总专注时间：{total_focus_time // 60} 分钟\n\n"
        report += "按待办事项统计：\n"
        for todo_id, focus_time in todo_focus_time.items():
            title = todo_dict.get(todo_id, "未知")
            report += f"待办 '{title}' (ID: {todo_id})：{focus_time // 60} 分钟\n"
        report += "\n按日期统计：\n"
        for day, focus_time in sorted(daily_focus_time.items()):
            report += f"{day}：{focus_time // 60} 分钟\n"

        self.analytics_text.insert(tk.END, report)