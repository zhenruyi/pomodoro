import sqlite3
import time
import os

class Database:
    def __init__(self, db_path="../data/database.sqlite"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def initialize(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

            # create todos table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    period TEXT NOT NULL,
                    created_at REAL NOT NULL)
            """)

            # create pomodoros table
            self.cursor.execute("""
                create table if not exists pomodoros(
                    id integer primary key autoincrement,
                    todo_id integer,
                    duration integer not null,
                    start_time real not null,
                    session_type text not null,
                    foreign key (todo_id) references todos(id))
            """)

            self.conn.commit()


        except sqlite3.OperationalError as e:
            print(f"数据库错误：{e}")
            print(f"无法打开数据库文件：{self.db_path}")
            print("请检查目录权限或路径是否正确。")
            raise

    def add_todo(self, title, content, period):
        self.cursor.execute("insert into todos(title, content, period, created_at) values (?, ?, ?, ?)", (title, content, period, time.time()))
        self.conn.commit()

    def get_todos(self):
        self.cursor.execute("select id, title, content, period from todos")
        return self.cursor.fetchall()

    def delete_todo(self, todo_id):
        self.cursor.execute("delete from todos where id = ?", (todo_id,))
        self.conn.commit()

    def add_pomodoro(self, todo_id, duration, start_time, session_type):
        self.cursor.execute("insert into pomodoros(todo_id, duration, start_time, session_type) values (?, ?, ?, ?)", (todo_id, duration, start_time, session_type))
        self.conn.commit()

    def get_pomodoros(self):
        self.cursor.execute("select todo_id, duration, start_time, session_type from pomodoros")
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()