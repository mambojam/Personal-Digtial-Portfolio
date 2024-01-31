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

    c.execute('SELECT * FROM todo_list')
    todos = c.fetchall()
    # Get column names dynamically
    columns = [column[0] for column in c.description]
    # Convert the list of tuples to a list of dictionaries
    todos = [dict(zip(columns, row)) for row in todos]
    
    conn.close()
    return todos

def add_todo(todo_to_add):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    c.execute('INSERT INTO todo_list (task_description) VALUES (?)', (todo_to_add,))
    # new_todo_id = c.execute(f'SELECT task_id from todo_list WHERE task_description = {todo_to_add}')
    new_todo_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]  # Get the last inserted ID
    conn.commit()
    conn.close()
    print("New todo added successfully")
    return new_todo_id

def update_todo(todo_to_update):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor

    c.execute(f'UPDATE todo_list SET task_description = {todo_to_update}, WHERE task_id = {todo_id}' )

    conn.commit()
    conn.close()

def complete_todo(todo):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor

    c.execute(f'UPDATE todo_list SET task_completed = 1, WHERE task_id = {todo_id}' )

    conn.commit()
    conn.close()
    return "Complete todo function executed"





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
