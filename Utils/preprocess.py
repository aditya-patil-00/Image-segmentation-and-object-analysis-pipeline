# preprocessing.py
from PIL import Image

def preprocess(image_path):
    image = Image.open(image_path).convert("RGB")
    return image