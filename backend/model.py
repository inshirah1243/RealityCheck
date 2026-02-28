import torch
import numpy as np
import cv2

from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# ===============================
# MODEL SETUP
# ===============================

model_name = "dima806/deepfake_vs_real_image_detection"

processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

model.eval()

# ===============================
# PREDICTION FUNCTION
# ===============================

def predict_frame(image_input):
    """
    Accepts:
        - image path (string)
        - numpy array (face crop from OpenCV)

    Returns:
        deepfake probability (float)
    """

    # If numpy array (face crop from OpenCV)
    if isinstance(image_input, np.ndarray):
        # Convert BGR (OpenCV) to RGB
        image = Image.fromarray(cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB))

    # If file path
    elif isinstance(image_input, str):
        image = Image.open(image_input).convert("RGB")

    else:
        raise ValueError("Unsupported image input type")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)

    # Class index 1 = deepfake
    deepfake_probability = probs[0][1].item()

    return float(deepfake_probability)