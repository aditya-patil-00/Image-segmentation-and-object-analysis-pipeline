import os
import shutil
import streamlit as st
from PIL import Image
import pandas as pd
import sqlite3

# Import your models here
from models.segmentation_model import process_image
from models.identification_model import update_descriptions, add_description_column
from models.text_extraction import extract_and_store_text, add_text_column
from models.summarization_model import summarize

from Utils.annotations import generate_annotated_image

def clear_output(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir, exist_ok=True)

def file_upload_section():
    st.title("Object Segmentation and Analysis Pipeline")
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        input_dir = os.path.join("..", "data", "input_images")
        clear_output(input_dir)
        image_path = os.path.join(input_dir, "input_image.jpg")
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(image_path, caption="Uploaded Image", use_column_width=True)
        return image_path

    return None

def display_segmented_image():
    segmented_image_path = os.path.join("..", "data", "output", "segmented_image.jpg")
    if os.path.exists(segmented_image_path):
        st.image(segmented_image_path, caption="Segmented Image", use_column_width=True)
    else:
        st.write("Segmented image not available.")

def display_object_details(display_size, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT object_id, save_path, description, text_data, summary FROM segmented_image_objects")
    data = cursor.fetchall()
    
    for object_id, save_path, description, text_data, summary in data:
        if os.path.exists(save_path):
            image = Image.open(save_path)
            st.image(image, caption=f"Object ID: {object_id}", width=display_size[0], use_column_width=False)
        else:
            st.write(f"Image not found for Object ID: {object_id}")

        st.write(f"**Description**: {description}")
        st.write(f"**Extracted Text**: {text_data}")
        st.write(f"**Summary**: {summary}")
        st.write("---")
    
    conn.close()

def display_final_output_table(db_path):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM segmented_image_objects", conn)
    st.write("### Mapped Data for Each Object")
    st.dataframe(df)
    conn.close()

def display_annotated_image(output_path):
    annotated_image_path = os.path.join(output_path, "annotated_image.jpg")
    if os.path.exists(annotated_image_path):
        st.image(annotated_image_path, caption="Annotated Image", use_column_width=True)
    else:
        st.write("Annotated image not available.")
