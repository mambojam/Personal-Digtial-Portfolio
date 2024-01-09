from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os
import copy
from functions import get_todos, write_todos
import gunicorn

app = Flask(__name__)

projects_data = [
    
        {   'html': 'store.html',
            'title': 'Online Store',
            'description': "When I first started learning SQL, I set up a simple DB for online outdoor clothes store. I've now moved this into SQLite and used Flask, JINJA and HTML forms to generate a query and display results on the webpage",
            'image': 'static/images/store.png'
        },
        {   
            'html': 'todo.html',
            'title': 'Todo List',
            'description': "I learnt the basics of Python following a Udemy course. The first part of the course involved designing a todo list application on the command line. I've built a front-end for this now and used some AJAX functions to dynamically manage user input on the front-end and a Flask server which manages the storage of the forms",
            'image': 'static/images/todo.png'
        },
        {   
            'html': 'comingsoon.html',
            'title': 'Game coming soon..',
            'description': "I've always been a big gamer, and so developing my own mini-games was a must once I'd learned the basics of programming. Using PyGame I developed a Pong game - it still has some bugs which I haven't had time to fix, but has a functioning, user controlled paddle, a ball that spawns and travels at a random trajectory within a range and a scroe tracker",
            'image': 'static/images/pong.png'
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

@app.route('/comingsoon', methods=['GET'])
def comingsoon():
    return render_template('comingsoon.html')

if __name__ == '__main__':
    app.run(debug=True)


## need to add images and work on the display next, also need to take the underscores out of names and swap for spaces
## need to set default params