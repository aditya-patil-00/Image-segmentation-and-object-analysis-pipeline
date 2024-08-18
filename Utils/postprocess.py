import os
from PIL import Image

def filter_detections(detections, threshold=0.5):
    # Filter out detections below the threshold
    boxes, labels, scores = detections
    indices = [i for i, score in enumerate(scores) if score > threshold]
    return [boxes[i] for i in indices], [labels[i] for i in indices], [scores[i] for i in indices]

import sqlite3

def extract_and_save_objects(image, boxes, save_dir, db_path, master_id="img_01"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for i, box in enumerate(boxes):
        # Extract bounding box coordinates
        xmin, ymin, xmax, ymax = map(int, box.tolist())
        
        # Crop the object from the image
        cropped_object = image.crop((xmin, ymin, xmax, ymax))
        
        # Create a unique object ID
        object_id = f"{master_id}_obj_{i+1}.jpg"
        save_path = os.path.join(save_dir, object_id)
        
        # Save the cropped object image
        cropped_object.save(save_path)

        # Insert metadata into the SQLite database
        cursor.execute('''
        INSERT INTO segmented_objects (master_id, object_id, xmin, ymin, xmax, ymax, save_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (master_id, object_id, xmin, ymin, xmax, ymax, save_path))

    conn.commit()
    conn.close()
