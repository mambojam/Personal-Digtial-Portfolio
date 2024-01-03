from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import os
from PIL import Image
from io import BytesIO
import base64
import copy

conn = sqlite3.connect('Online_Store_DB.db')
cur = conn.cursor()

# create the query
query = "SELECT image FROM Product WHERE product_name = 'Scarpa_Quantix_SF'"

# execute query and retrieve results
cur.execute(query)
blob_data = cur.fetchone()[0]
print(len(blob_data))

# Convert the BLOBs to Base-64
image = Image.open(BytesIO(blob_data))  # converts blob back to image
image.show()  # Display the image
image_base64 = base64.b64encode(image.tobytes()).decode('utf-8')
image = image_base64
print(len(image))

print("hello")

conn.close()
