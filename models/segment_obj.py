import sqlite3
import os

def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table to store segmented object metadata
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS segmented_image_objects(
        master_id TEXT,
        object_id TEXT PRIMARY KEY,
        xmin INTEGER,
        ymin INTEGER,
        xmax INTEGER,
        ymax INTEGER,
        save_path TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Define the database path
curr_dir = os.getcwd()
par_dir = os.path.dirname(curr_dir)
db_path = os.path.join(par_dir, 'data', 'segmented_image_objects.db')

create_database(db_path)