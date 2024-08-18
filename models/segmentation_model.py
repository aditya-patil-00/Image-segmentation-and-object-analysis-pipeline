import torch
from transformers import AutoImageProcessor, DetrForSegmentation
from PIL import Image
import os
import sys

curr_dir = os.getcwd()
par_dir = os.path.dirname(curr_dir)
#utils_dir = os.path.join(par_dir, 'Utils')
sys.path.append(par_dir)
#print(utils_dir)

from Utils.preprocess import preprocess
from Utils.visualization import visualize_segments
from Utils.postprocess import extract_and_save_objects
from models import segment_obj

def load_model():
    # Load pre-trained DETR model and processor
    processor = AutoImageProcessor.from_pretrained("facebook/detr-resnet-50-panoptic")
    model = DetrForSegmentation.from_pretrained("facebook/detr-resnet-50-panoptic")
    model.eval()
    return model, processor

def segment(model, processor, image):
    # Preprocess the image and make predictions
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    
    # Post-process and extract results
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # Extract masks, boxes, labels, and scores
    boxes = results["boxes"]
    labels = results["labels"]
    scores = results["scores"]

    return boxes, labels, scores

def main(image_path):

    curr_dir = os.getcwd()
    par_dir = os.path.dirname(curr_dir)
    db_path = os.path.join(par_dir, 'data', 'segmented_objects.db')

    segment_obj.create_database(db_path)

    # Load the segmentation model and processor
    model, processor = load_model()
    # Preprocess the image
    image = preprocess(image_path)  # This should return a PIL image
    # Perform segmentation
    boxes, labels, scores = segment(model, processor, image)
    # Prepare the output path
    out_path = os.path.join(par_dir, 'data', 'output', 'segmented.jpg')
    # Visualize and save the segmented image
    visualize_segments(image_path, boxes, labels, scores, output_path=out_path)

    # Extract and save each object
    segmented_objects_dir = os.path.join(par_dir, 'data', 'segmented_objects')
    extract_and_save_objects(image, boxes, segmented_objects_dir, db_path)

img_path = os.path.join(par_dir, 'data', 'input_images', 'sample image.jpg')

if __name__ == "__main__":
    image_path = img_path
    print(image_path)
    main(image_path)