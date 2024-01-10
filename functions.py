import sqlite3

# def get_todos(filepath='static/todos.txt'):
#     """ Read todos.txt file and return the list of todo items within it """
#     with open(filepath, 'r') as file_local:
#         todos_local = file_local.readlines()
#     return todos_local

#   # file = open('todos.txt', 'r')
#            # todos = file.readlines()
#            # file.close()

#         #with open('todos.txt', 'r') as file:
#          #   todos = file.readlines()

# def write_todos(todos_arg, filepath='static/todos.txt'):
#     """ Write the todo list items in the text file """
#     with open(filepath, 'w') as file:
#         file.writelines(todos_arg)


# if __name__ == "__main__":
#     print(todos)

# Additional functions
# Database initialization
def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # Create the todo_list table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS todo_list (
            task_id INTEGER PRIMARY KEY,
            task_description TEXT NOT NULL,
            is_completed INTEGER DEFAULT 0,
            due_date DATE
        )
    ''')

    conn.commit()
    conn.close()

# Get all todos from the database
def get_todos():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    c.execute('SELECT task_description FROM todo_list')
    todos = [row[0] for row in c.fetchall()]

    conn.close()
    return todos

# Write todos to the database
def write_todos(todos):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # Clear existing todos
    c.execute('DELETE FROM todo_list')

    # Insert new todos
    for todo in todos:
        c.execute('INSERT INTO todo_list (task_description) VALUES (?)', (todo,))

    conn.commit()
    conn.close()