import os
import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
import sqlite3

# Load the BLIP model
def load_captioning_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")   
    return model, processor

# Function to generate descriptions using BLIP
def generate_description(model, processor, object_image_path):
    image = Image.open(object_image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

def add_description_column(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(segmented_image_objects)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'description' not in columns:
        cursor.execute('''
            ALTER TABLE segmented_image_objects
            ADD COLUMN description TEXT
        ''')
        print("Added 'description' column to 'segmented_image_objects' table.")
    else:
        print("'description' column already exists.")
    
    conn.commit()
    conn.close()

def update_descriptions(db_path):
    # Load the captioning model
    model, processor = load_captioning_model()

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all objects that need identification
    cursor.execute("SELECT object_id, save_path FROM segmented_image_objects WHERE description is NULL")
    objects = cursor.fetchall()

    for object_id, save_path in objects:
        description = generate_description(model, processor, save_path)
        cursor.execute('''
            UPDATE segmented_image_objects
            SET description = ?
            WHERE object_id = ?
        ''', (description, object_id))
        print(f"Object {object_id} description generated: {description}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    curr_dir = os.getcwd()
    par_dir = os.path.dirname(curr_dir)
    db_path = os.path.join(par_dir, 'data', 'segmented_objects2.db')
    add_description_column(db_path)
    update_descriptions(db_path)