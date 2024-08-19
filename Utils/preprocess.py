# preprocessing.py
from PIL import Image, ImageEnhance
import numpy as np
import cv2

def preprocess(image_path):
    image = Image.open(image_path).convert("RGB")
    return image