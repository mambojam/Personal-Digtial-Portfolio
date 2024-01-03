from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os
from PIL import Image
from io import BytesIO
import base64
import copy

app = Flask(__name__)

projects_data = [
    
        {   'html': 'store.html',
            'title': 'Online Store',
            'description': 'When I first started learning SQL, I set up a simple DB for online outdoor clothes store. I\'ve now moved this into SQLite and used Flask, JINJA and HTML forms to generate a query and display results on the webpage',
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

# @app.route('/searchItems', methods=['POST'])
# def loadItems():
#     categories = json.loads(request.form['categories']) # turn the JSON string back into a list
#     min_price = request.form['minPrice']
#     max_price = request.form['maxPrice']
   
#     try:
#         conn = sqlite3.connect('Online_Store_DB.db') 
#         cur = conn.cursor()

#         # create the query 
#         query = "SELECT * FROM Product WHERE "
#         category_conditions = " OR ".join(["category = ?" for category in categories])
#         query += f"price BETWEEN ? AND ? AND ({category_conditions})"
        
#         # execute query and retrieve results
#         res = cur.execute(query, [min_price, max_price] + categories)
#         productlist = res.fetchall()

#         # Get column names dynamically
#         columns = [column[0] for column in cur.description]

#         # Convert the list of tuples to a list of dictionaries
#         all_products = [dict(zip(columns, row)) for row in productlist]
#         # Convert the BLOBs to Base-64
#         for product in all_products:
#             blob_data = product["image"]
#             image = Image.open(BytesIO(blob_data)) #converts blob back to image
#             image_base64 = base64.b64encode(image.read()).decode('utf-8') # converts image back to base-64
            

#     except sqlite3.Error as e:
# 	    logging.error(f"SQLite Error: {e}")
        
#     finally:
#         conn.close()
#         return jsonify(all_products[]), image_base64

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

@app.route('/render_image', methods=['GET'])
def render_image():
    conn = sqlite3.connect('Online_Store_DB.db') 
    cur = conn.cursor()

    # create the query 
    query = "SELECT image FROM Product WHERE product_name = 'Scarpa_Quantix_SF'"
    
    # execute query and retrieve results
    cur.execute(query)
    blob_data = cur.fetchone()


    # Convert the BLOBs to Base-64
    image = Image.open(BytesIO(blob_data)) #converts blob back to image
    image_base64 = base64.b64encode(image.read()).decode('utf-8') # converts image back to base-64
    image = image_base64
    print("hello")
    app.logger.info(f"Product name: {product.product_name} Base64 length: {len(product.image)}")
    
    conn.close()
    return render_template("image.html", image=image)

if __name__ == '__main__':
    app.run(debug=True)


## need to add images and work on the display next, also need to take the underscores out of names and swap for spaces
## need to set default params