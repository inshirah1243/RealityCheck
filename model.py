import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import timm

# Load pretrained EfficientNet
model = timm.create_model("efficientnet_b0", pretrained=True)
model.eval()

# Add simple binary classification head logic
# We simulate deepfake probability using feature activations
def predict_frame(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        features = model.forward_features(input_tensor)
        pooled = torch.mean(features)
        score = torch.sigmoid(pooled).item()

    return float(score)