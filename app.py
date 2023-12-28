from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os

app = Flask(__name__)

projects_data = [
    
        {   'html': 'store.html',
            'title': 'Online Store',
            'description': 'When I first started learning SQL, I set up a simple DB for online outdoor clothes store. I\'ve now design and integrated a front end for it.',
            'image': 'static/project1.jpg'
        },
        {   
            'html': 'game.html',
            'title': 'Project 2',
            'description': 'Description of Project 2.',
            'image': 'static/project2.jpg'
        }
        
]

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)

@app.route('/project/<string:html_file>')
def project_detail(html_file):
    return render_template(html_file)

@app.route('/searchItems', methods=['POST'])
def loadItems():
    categories = json.loads(request.form['categories']) # turn the JSON string back into a list
    min_price = request.form['minPrice']
    max_price = request.form['maxPrice']
   
    try:
        conn = sqlite3.connect('Online_Store_DB.db')
        cur = conn.cursor()

        # create the query 
        query = "SELECT * FROM Product WHERE "
        category_conditions = " OR ".join(["category = ?" for _ in categories])
        query += f"price BETWEEN ? AND ? AND ({category_conditions})"
        print(query)
        res = cur.execute(query, [min_price, max_price] + categories)
        print(res)
        productlist = res.fetchall()
        # Get column names dynamically
        columns = [column[0] for column in cur.description]
        # Convert the list of tuples to a list of dictionaries
        all_products = [dict(zip(columns, row)) for row in productlist]

    except sqlite3.Error as e:
	    logging.error(f"SQLite Error: {e}")
        
    finally:
        conn.close()
        return jsonify(all_products)

@app.route('/test', methods=['GET'])
def getimages():
    conn = sqlite3.connect('Online_Store_DB.db')
    cur = conn.cursor()
    query = "SELECT * FROM Images"
    res = cur.execute(query)
    productlist = res.fetchall()
    return jsonify(productlist)


if __name__ == '__main__':
    app.run(debug=True)


## need to add images and work on the display next, also need to take the underscores out of names and swap for spaces
## need to set default params