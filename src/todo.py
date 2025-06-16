class TodoManager:
    def __init__(self, db):
        self.db = db

    def add_todo(self, title, content, period = "none"):
        self.db.add_todo(title, content, period)

    def list_todos(self):
        return self.db.get_todos()

    def delete_todo(self, todo_id):
        self.db.delete_todo(todo_id)