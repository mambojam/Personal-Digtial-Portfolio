from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os
from PIL import Image
from io import BytesIO
import base64
import copy
from functions import get_todos, write_todos

app = Flask(__name__)

projects_data = [
    
        {   'html': 'store.html',
            'title': 'Online Store',
            'description': 'When I first started learning SQL, I set up a simple DB for online outdoor clothes store. I\'ve now moved this into SQLite and used Flask, JINJA and HTML forms to generate a query and display results on the webpage',
            'image': 'static/images/project1.jpg'
        },
        {   
            'html': 'todo.html',
            'title': 'Project 2',
            'description': 'Description of Project 2.',
            'image': 'static/images/project2.jpg'
        },
        {   
            'html': 'game.html',
            'title': 'Project 3',
            'description': 'Description of Project 2.',
            'image': 'static/images/project3.jpg'
        }   
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

@app.route('/project/<string:html_file>')
def project_detail(html_file):
    if html_file == "todo.html":
        todos = get_todos()
        return render_template("todo.html", todos=todos)
    return render_template(html_file)

@app.route('/searchItems', methods=['GET', 'POST'])
def loadItems():
    if request.method == 'GET':
        return render_template("store.html")

    elif request.method == 'POST':

        categories = request.form.getlist('category')
        if categories == []:
            categories = ["Rock_Shoe","Rope","Harness","Quickdraw"]
        min_price = request.form['minPrice']
        if min_price == "":
            min_price = "0"
        max_price = request.form['maxPrice']
        if max_price == "":
            max_price = "10000"

    
        try:
            conn = sqlite3.connect('Online_Store_DB.db') 
            cur = conn.cursor()

            # create the query 
            query = "SELECT * FROM Product WHERE "
            category_conditions = " OR ".join(["category = ?" for category in categories])
            query += f"price BETWEEN ? AND ? AND ({category_conditions})"
            
            # execute query and retrieve results
            res = cur.execute(query, [min_price, max_price] + categories)
            productlist = res.fetchall()

            # Get column names dynamically
            columns = [column[0] for column in cur.description]

            # Convert the list of tuples to a list of dictionaries
            all_products = [dict(zip(columns, row)) for row in productlist]

        except sqlite3.Error as e:
            logging.error(f"SQLite Error: {e}")
            
        finally:
            conn.close()
            return render_template("response.html", all_products=all_products)

# @app.route('/render_image', methods=['GET'])
# def render_image():
#     conn = sqlite3.connect('Online_Store_DB.db') 
#     cur = conn.cursor()

#     # create the query 
#     query = "SELECT image FROM Product WHERE product_name = 'Scarpa_Quantix_SF'"
    
#     # execute query and retrieve results
#     cur.execute(query)
#     blob_data = cur.fetchone()


#     # Convert the BLOBs to Base-64
#     image = Image.open(BytesIO(blob_data)) #converts blob back to image
#     image_base64 = base64.b64encode(image.read()).decode('utf-8') # converts image back to base-64
#     image = image_base64
#     print("hello")
#     app.logger.info(f"Product name: {product.product_name} Base64 length: {len(product.image)}")
    
#     conn.close()
#     return render_template("image.html", image=image)

@app.route('/AddTodo', methods=['GET', 'POST'])
def addtodo():
    if request.method == 'GET':
        todos = get_todos()
        render_template("todo.html", todos=todos)




    if request.method == 'POST':
        todo = request.form['todo']
        todos = get_todos()
        todos.append(todo + '\n')
        write_todos(todos)
        return todo


@app.route('/UpdateTodo', methods=['POST'])
def updatetodo():
    todos = request.json
    print(todos)
    saved_todos = []
    for todo in todos:
        if todo.endswith("\n"):
            saved_todos.append(todo)
        else:
        	saved_todos.append(todo + " \n")

    write_todos(saved_todos)
    return "Todos updated successfully"

@app.route('/to_do', methods=('GET', 'POST'))
def todos():
    
    while True:
        user_action = input("Type add, show, edit, complete or exit: ")
        user_action = user_action.strip()

        if user_action.startswith("add"):
            todo = (user_action[4:])

            todos = get_todos()

            todos.append(todo + '\n')

            write_todos(todos)

        elif user_action.startswith("show"):
            todos = get_todos()

                # new_todos = [item.strip('\n') for item in todos]
                # above is a list comprehension which simplifies a section to remove the break line
                # however we can make it even more simple using the strip function as below:

            for index, item in enumerate(todos):
                item = item.strip('\n')
                row = f"{index +1}.{item}"
                print(row)

        elif user_action.startswith('edit'):
            try:
                number = int(user_action[5:])
                print(number)

                number = number - 1

                todos = get_todos()

                new_todo = input("Enter new todo: ")
                todos[number] = new_todo + '\n'

                write_todos(todos)

            except ValueError:
                print("Invalid command")
                continue

        elif user_action.startswith('complete'):

            try:
                number = int(user_action[9:])

                todos = get_todos()

                index = number - 1
                todo_to_remove = todos[index].strip('\n')
                todos.pop(index)

                write_todos(todos)

                message = f"{todo_to_remove} was removed from the list"
                print(message)
            except IndexError:
                print("no item with corresponding number")
                continue

        elif user_action.startswith('exit'):
            break
        else:
            print("Invalid command")

    print("Bye!")


if __name__ == '__main__':
    app.run(debug=True)


## need to add images and work on the display next, also need to take the underscores out of names and swap for spaces
## need to set default params