import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(data_tuple):
    try:
        conn = sqlite3.connect('Online_Store_DB.db', timeout=10)
        cur = conn.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO Product
                                  (product_name, category, price, image) VALUES (?, ?, ?, ?)"""

        blob_image = convertToBinaryData(data_tuple[3])
        blob_data_list = []
        for num in range(len(data_tuple)):
            if num == 3:
                blob_data_list.append(blob_image)
            else:
                blob_data_list.append(data_tuple[num])
        
        cur.execute(sqlite_insert_blob_query, blob_data_list)
        conn.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")


values = [
('Scarpa_Quantix_SF', 'Rock_Shoe', 105.00, 'static/images/shoe.jpg'),
('Scarpa_Mago', 'Rock_Shoe', 99.00, 'static/images/shoe.jpg'),
('La_Sportiva_TC_Pro', 'Rock_Shoe', 155.00, 'static/images/shoe.jpg'),
('La_Sportiva_Skwama', 'Rock_Shoe', 130.00, 'static/images/shoe.jpg'),
('La_Sportiva_Miura_Lace', 'Rock_Shoe', 127.00, 'static/images/shoe.jpg'),
('Mammut_9.5MM_50M', 'Rope', 112.00, 'static/images/rope.jpg'),
('Edelweiss_9.2MM_70M', 'Rope', 212.00, 'static/images/rope.jpg'),
('Edelrid_Eco_50M', 'Rope', 157.50, 'static/images/rope.jpg'),
('Beal_Phantom', 'Harness', 54.00, 'static/images/harness.jpg'),
('DMM_Centre', 'Harness', 58.50, 'static/images/harness.jpg'),
('DMM_Centre', 'Harness', 58.50, 'static/images/harness.jpg'),
('Ocun_Webee_Bigwall', 'Harness', 85.50, 'static/images/harness.jpg'),
('Mammut_Bionic_5_Pack', 'Quickdraw', 82.50, 'static/images/quickdraw.jpg'),
('Black_Diamond_6_Pack', 'Quickdraw', 85.50, 'static/images/quickdraw.jpg'),
('DMM_Alpha_6_Pack', 'Quickdraw', 128.00, 'static/images/quickdraw.jpg')
]

for value in values:
    insertBLOB(value)

# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')
# insertBLOB('Scarpa_Vapour_S', 'Rock_Shoe', 125.00, 'static/images/shoe.jpg')