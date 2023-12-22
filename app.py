from flask import Flask, render_template, request
import sqlite3

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
    categories = request.form['categories']
    minPrice = request.form['minPrice']
    maxPrice = request.form['maxPrice']
    try:
        conn = sqlite3.connect('Online_Store_DB.db')
        cur = conn.cursor()
        query = "SELECT * FROM Products "
        for num in range(len(categories)):
            if num == 0:
                query += "WHERE "
            else:
                query += "OR "
            query += "category = \"" + categories[num] + "\" AND " + int(minPrice) + " < price AND price < " + int(maxPrice)
        res = cur.execute(query)
    except:
	    res = "error in finding items"
    finally:
        conn.close()
        return msg

if __name__ == '__main__':
    app.run(debug=True)
