from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os
import copy
from functions import init_db, get_todos, write_todos
import gunicorn

app = Flask(__name__)

# Use this to get the project data for JINJA templating projects page
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

# Homepage
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

# Get into the project
@app.route('/project/<string:html_file>')
# html_file is dynamically generated for project['html']
def project_detail(html_file):
    # todo homepage needs the todos as parameters
    if html_file == "todo.html":
        init_db()
        todos = get_todos()
        return render_template("todo.html", todos=todos)
    return render_template(html_file)

# store homepage
@app.route('/searchItems', methods=['GET', 'POST'])
def loadItems():
    if request.method == 'GET':
        return render_template("store.html")
# GEt items from db
    elif request.method == 'POST':
# Set default parameters
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

# Todo list 

@app.route('/AddTodo', methods=['GET', 'POST'])
def addtodo():
    # another route to todos homepage
    if request.method == 'GET':
        init_db()
        todos = get_todos()
        render_template("todo.html", todos=todos)
    # write new todo to db
    if request.method == 'POST':
        init_db()
        todo = request.form['todo']
        todos = get_todos()
        todos.append(todo)
        write_todos(todos)
        return todo

# re-write todos
@app.route('/UpdateTodo', methods=['POST'])
def updatetodo():
    init_db()
    todos = request.json
    write_todos(todos)
    return "Todos updated successfully"

# template for pages still in development
@app.route('/comingsoon', methods=['GET'])
def comingsoon():
    return render_template('comingsoon.html')

if __name__ == '__main__':
    app.run(debug=True)

