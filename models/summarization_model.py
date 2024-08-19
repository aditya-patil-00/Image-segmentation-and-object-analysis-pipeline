import sqlite3
import os
from transformers import pipeline

def load_summarization_model():
    summarizer = pipeline("summarization", max_length = 15, min_length = 5, model="facebook/bart-large-cnn")
    return summarizer

def generate_summary(summarizer, text):
    summary = summarizer(text, do_sample=False)
    return summary[0]['summary_text']

def add_summary_column(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the 'summary' column already exists
    cursor.execute("PRAGMA table_info(segmented_objects2)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'summary' not in columns:
        # Add the 'summary' column if it doesn't exist
        cursor.execute('''
            ALTER TABLE segmented_objects2
            ADD COLUMN summary TEXT
        ''')
        print("Added 'summary' column to 'segmented_objects2' table.")
    else:
        print("'summary' column already exists.")
    
    conn.commit()
    conn.close()

def summarize_and_store(db_path, summarizer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT object_id, description, text_data FROM segmented_objects2")
    objects = cursor.fetchall()

    for object_id, description, text_data in objects:
        combined_text = f"Description : {description}. Extracted Text : {text_data}"
        summary = generate_summary(summarizer, combined_text)
        cursor.execute('''
            UPDATE segmented_objects2
            SET summary = ?
            WHERE object_id = ?
        ''', (summary, object_id))
        print(f"Object {object_id} summary generated: {summary}")

    conn.commit()
    conn.close()

def main():
    curr_dir = os.getcwd()
    par_dir = os.path.dirname(curr_dir)
    db_path = os.path.join(par_dir, 'data', 'segmented_objects2.db')

    # Load the summarization model
    summarizer = load_summarization_model()

    # Step 1: Add 'summary' column to the database if it doesn't exist
    add_summary_column(db_path)

    # Step 2: Generate and store summaries in the database
    summarize_and_store(db_path, summarizer)

if __name__ == "__main__":
    main()
