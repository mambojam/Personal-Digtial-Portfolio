import sqlite3
from flask import Flask, render_template, request, jsonify
import json
from PIL import Image
from io import BytesIO
import base64



try:
    # create a connection and a cursor
    conn = sqlite3.connect('Online_Store_DB.db') 
    cur = conn.cursor()

    # create the query 
    query = "SELECT * FROM Product WHERE price BETWEEN 50 AND 150 AND category = \"Rock_Shoe\""

    # execute query and retrieve results
    res = cur.execute(query)
    productlist = res.fetchall()

    display_items = productlist


    print(productlist[0])
    # Get column names dynamically
    columns = [column[0] for column in cur.description]

    # Convert the list of tuples to a list of dictionaries
    all_products = [dict(zip(columns, row)) for row in productlist]

    # Convert the BLOBs to Base-64
    for product in all_products:
        blob_data = product["image"]
        image = Image.open(BytesIO(blob_data)) #converts blob back to image
        image_base64 = base64.b64encode(image.read()).decode('utf-8') # converts image back to base-64
        product["image"] = image_base64



#     # convert the BLOBs into a base 64 string
#     newproductlist = productlist.deepcopy(productlist)
#     print(newproductlist)

#     # Image.open(BytesIO(blob_data))
#     
#     # Can't return JSONified BLOBs so need to change the image back here



except sqlite3.Error as e:
    logging.error(f"SQLite Error: {e}")

finally:
    conn.close()
    # jsonify(all_products) ###