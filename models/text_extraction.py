import sqlite3
import os
import easyocr
from PIL import Image
import sys
import numpy as np

curr_dir = os.getcwd()
par_dir = os.path.dirname(curr_dir)
sys.path.append(par_dir)

def add_text_column(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the 'text_data' column already exists
    cursor.execute("PRAGMA table_info(segmented_objects2)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'text_data' not in columns:
        # Add the 'text_data' column if it doesn't exist
        cursor.execute('''
            ALTER TABLE segmented_objects2
            ADD COLUMN text_data TEXT
        ''')
        print("Added 'text_data' column to 'segmented_objects2' table.")
    else:
        print("'text_data' column already exists.")
    
    conn.commit()
    conn.close()

def extract_text_from_image(image_path):

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_path)
    text = ' '.join([res[1] for res in results])

    return text

def extract_and_store_text(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT object_id, save_path FROM segmented_objects2")
    objects = cursor.fetchall()

    for object_id, save_path in objects:
        text_data = extract_text_from_image(save_path)
        print(text_data)
        cursor.execute('''
            UPDATE segmented_objects2
            SET text_data = ?
            WHERE object_id = ?
        ''', (text_data, object_id))
        print(f"Object {object_id} text extracted: {text_data}")

    conn.commit()
    conn.close()

def main():
    curr_dir = os.getcwd()
    par_dir = os.path.dirname(curr_dir)
    db_path = os.path.join(par_dir, 'data', 'segmented_objects2.db')

    # Step 1: Add 'text_data' column to the database if it doesn't exist
    add_text_column(db_path)

    # Step 2: Extract text from images and store it in the database
    extract_and_store_text(db_path)

if __name__ == "__main__":
    main()