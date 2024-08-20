from PIL import Image, ImageDraw, ImageFont
import os
import sqlite3

curr_dir = os.getcwd()
par_dir = os.path.dirname(curr_dir)

def generate_annotated_image(image_path, db_path, output_path):
    # Open the original image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Load a font for the annotations
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Connect to the database and fetch object details
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT object_id, xmin, ymin, xmax, ymax FROM segmented_image_objects")
    objects = cursor.fetchall()

    # Loop through each object and draw the bounding box and label
    for obj in objects:
        object_id, xmin, ymin, xmax, ymax = obj
        
        # Draw the bounding box
        draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=2)
        
        # Add the label (object ID in this case)
        draw.text((xmin, ymin), object_id, fill="white", font=font)
    
    conn.close()
    
    # Save the annotated image
    annotated_image_path = os.path.join(output_path, "annotated_image.jpg")
    image.save(annotated_image_path)
    return annotated_image_path

# Example usage:
#image_path = os.path.join(par_dir, 'data', 'input_images', 'input_image.jpg')
#db_path = os.path.join(par_dir, 'data', 'segmented_image_objects.db')
#output_path = os.path.join(par_dir, 'data', 'output')
#
#annotated_image_path = generate_annotated_image(image_path, db_path, output_path)
