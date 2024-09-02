<h1 align="center" id="title">Object Segmentation and Analysis Pipeline</h1>

<p id="description">The Object Segmentation and Analysis Pipeline is a comprehensive application designed to process and analyze images through a series of machine learning models. The pipeline includes functionalities for image segmentation object identification text extraction and summarization. It provides a Streamlit-based web application for user interaction allowing users to upload images view segmented objects and analyze the results through an intuitive interface.</p>
  
<h2>Features and Architecture</h2>

Here're some of the project's best features:

*   Image Upload: Allows users to upload images for processing.
*   Segmentation: Processes images to identify and segment objects.
*   Object Analysis: Extracts text from segmented objects and updates descriptions.
*   Summarization: Generates summaries of the extracted data.
*   Visualization: Displays segmented images object details and final output in a user-friendly format.

![System Architecture](https://i.imgur.com/DJxqsEz.png)

<h2>Installation Steps:</h2>

<p>1. Clone the repository in your local device</p>

```
git clone https://github.com/aditya-patil-00/aditya-patil-wasserstoff-AiInternTask
```

<p>2. Create virtual env</p>

```
python -m venv myenv source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
```

<p>3. Install required packages</p>

```
pip install -r requirements.txt
```

<p>4. Run the streamlit app</p>

```
streamlit run app.py
```

<h2> Sample Screenshot </h2>

![Streamlit Interface](https://i.imgur.com/yEZ96IA.png)

<h2> License:</h2>

This project is licensed under the GPL-3.0 license
