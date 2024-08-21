import os
import streamlit as st

from components import (
    file_upload_section,
    display_segmented_image,
    display_object_details,
    display_final_output_table,
    display_annotated_image,
)
from models.segmentation_model import process_image
from Utils.annotations import generate_annotated_image
from models.identification_model import update_descriptions, add_description_column
from models.text_extraction import extract_and_store_text, add_text_column
from models.summarization_model import summarize

# Get the base directory (where the app.py is located)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the base directory
image_path = os.path.join(base_dir, '..', 'data', 'input_images', 'input_image.jpg')
db_path = os.path.join(base_dir, '..', 'data', 'segmented_image_objects.db')
output_path = os.path.join(base_dir, '..', 'data', 'output')

def main():
    image_path = file_upload_section()
    if image_path:
        process_image(image_path)
        display_segmented_image()

        generate_annotated_image(image_path, db_path, output_path)
        display_annotated_image(output_path)

        add_description_column(db_path)
        update_descriptions(db_path)
        add_text_column(db_path)
        extract_and_store_text(db_path)
        summarize(db_path)

        st.write("### Object Details")
        display_object_details(display_size=(100, 100), db_path=db_path)

        st.write("### Final Output")
        display_final_output_table(db_path=db_path)

if __name__ == '__main__':
    main()