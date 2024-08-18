import matplotlib.pyplot as plt
from PIL import Image

def visualize_segments(image_path, boxes, labels, scores, output_path):
    image = Image.open(image_path).convert("RGB")
    plt.figure(figsize=(12, 8))
    plt.imshow(image)

    ax = plt.gca()
    for box, label, score in zip(boxes, labels, scores):
        x0, y0, x1, y1 = box.tolist()
        rect = plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, color='red', linewidth=3)
        ax.add_patch(rect)
        ax.text(x0, y0, f'{label}: {score:.2f}', bbox=dict(facecolor='yellow', alpha=0.5))

    plt.axis('off')
    plt.savefig(output_path)
    plt.show()
