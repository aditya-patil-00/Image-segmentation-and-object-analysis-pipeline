import sqlite3
import os
import easyocr
from PIL import Image
import numpy as np

# Get the base directory (where text_extraction.py is located)
base_dir = os.path.dirname(os.path.abspath(__file__))

def add_text_column(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the 'text_data' column already exists
    cursor.execute("PRAGMA table_info(segmented_image_objects)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'text_data' not in columns:
        # Add the 'text_data' column if it doesn't exist
        cursor.execute('''
            ALTER TABLE segmented_image_objects
            ADD COLUMN text_data TEXT
        ''')
        print("Added 'text_data' column to 'segmented_image_objects' table.")
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

    cursor.execute("SELECT object_id, save_path FROM segmented_image_objects WHERE text_data is NULL")
    objects = cursor.fetchall()

    for object_id, save_path in objects:
        text_data = extract_text_from_image(save_path)
        print(text_data)
        cursor.execute('''
            UPDATE segmented_image_objects
            SET text_data = ?
            WHERE object_id = ?
        ''', (text_data, object_id))
        print(f"Object {object_id} text extracted: {text_data}")

    conn.commit()
    conn.close()

def main():
    db_path = os.path.join(base_dir, '..', 'data', 'segmented_image_objects.db')

    # Step 1: Add 'text_data' column to the database if it doesn't exist
    add_text_column(db_path)

    # Step 2: Extract text from images and store it in the database
    extract_and_store_text(db_path)

if __name__ == "__main__":
    main()
