from src.database import Database
import time


def test_database():
    db = Database()
    try:
        # 初始化数据库
        db.initialize()

        # 添加测试待办
        db.add_todo("测试任务", "这是一个测试", "daily")

        # 获取待办
        todos = db.get_todos()
        print("待办事项：", todos)

        # 添加番茄时钟记录
        if todos:
            todo_id = todos[0][0]
            db.add_pomodoro(todo_id, 25, time.time(), "focus")

        # 获取番茄时钟记录
        sessions = db.get_pomodoros()
        print("番茄时钟记录：", sessions)

    finally:
        db.close()


if __name__ == "__main__":
    test_database()