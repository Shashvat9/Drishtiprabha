# embedding.py

import torch
from torchvision import transforms
from PIL import Image
import numpy as np

# Example transform (modify based on your requirements)
transform = transforms.Compose([
    transforms.Resize((224, 224)),      # Resize to the size expected by the model
    transforms.ToTensor(),              # Convert PIL Image to Tensor
    transforms.Normalize(               # Normalize with ImageNet means and stds
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
    # Add more transforms if needed
])

def generate_image_embedding(image):
    """
    Generates an embedding for the given image.

    Args:
        image (numpy.ndarray): The input image in RGB format.

    Returns:
        torch.Tensor: The generated embedding.
    """
    if image is None:
        print("Warning: Received an empty image for embedding.")
        return None

    try:
        # Convert NumPy array (RGB) to PIL Image
        pil_image = Image.fromarray(image)

        # Apply transformations
        input_tensor = transform(pil_image).unsqueeze(0)  # Add batch dimension

        # Move tensor to the appropriate device (e.g., CPU or GPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_tensor = input_tensor.to(device)

        # Load your embedding model (ensure it's on the same device)
        # Example: Using a pre-trained ResNet model for embeddings
        model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        model.eval()
        model.to(device)

        with torch.no_grad():
            embedding = model(input_tensor)

        return embedding
    except Exception as e:
        print(f"Error generating image embedding: {e}")
        return None