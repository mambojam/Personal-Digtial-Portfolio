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

@app.route('/test')
def testSearch():
    conn = sqlite3.connect('Online_Store_DB.db')
    cur = conn.cursor()
    query = "SELECT * FROM Product"
    res = str(conn.execute(query))
    print(res)
    return res

# need to watch a tutorial on this as I'm getting stuck
# how to write a select query to return the data and add to the html

@app.route('/searchItems', methods=['POST'])
def loadItems():
    categories = json.loads(request.form['categories']) # turn the JSON string back into a list
    min_price = request.form['minPrice']
    max_price = request.form['maxPrice']
   
    try:
        conn = sqlite3.connect('Online_Store_DB.db')
        cur = conn.cursor()

        # query = "SELECT * FROM Products "
        # for num in range(len(categories)):
        #     if num == 0:
        #         query += "WHERE "
        #     else:
        #         query += "OR "
        #     query += "category = \"" + categories[num] + "\" "
        # query += "AND price BETWEEN (%s) and (%s)", [minPrice, maxPrice]    
    

        # create the query 
        query = "SELECT * FROM Product WHERE "
        category_conditions = " OR ".join(["category = ?" for _ in categories])
        query += f"price BETWEEN ? AND ? AND ({category_conditions})"
        print(query)
        res = cur.execute(query, [min_price, max_price] + categories)
        print(res)
        productlist = res.fetchall()

    except sqlite3.Error as e:
	    logging.error(f"SQLite Error: {e}")
        
    finally:
        conn.close()
        return jsonify(productlist)
        # return jsonify({'htmlresponse': render_template('response.html', productlist=productlist)})

if __name__ == '__main__':
    app.run(debug=True)


## getting this to return a list of items now - it's not the full list for some reason - need to work on
## making sure the querty is correct, then can look into adding images, and displaying the content properly