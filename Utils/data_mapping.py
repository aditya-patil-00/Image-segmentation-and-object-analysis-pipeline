import sqlite3
import json
import os

def export_to_json(db_path, json_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Select data from the existing tables
    cursor.execute('''
        SELECT object_id, master_id, description, text_data, summary
        FROM segmented_objects2
    ''')
    objects = cursor.fetchall()

    # Convert to a list of dictionaries
    objects_list = [
        {
            "object_id": row[0],
            "master_image_id": row[1],
            "description": row[2],
            "text_data": row[3],
            "summary": row[4]
        }
        for row in objects
    ]

    # Write to a JSON file
    with open(json_path, 'w') as f:
        json.dump(objects_list, f, indent=4)

    conn.close()

def main():
    curr_dir = os.getcwd()
    par_dir = os.path.dirname(curr_dir)
    db_path = os.path.join(par_dir, 'data', 'segmented_objects2.db')
    json_path = os.path.join(par_dir, 'data', 'object_mappings.json')

    # Export the database contents to a JSON file
    export_to_json(db_path, json_path)

if __name__ == "__main__":
    main()