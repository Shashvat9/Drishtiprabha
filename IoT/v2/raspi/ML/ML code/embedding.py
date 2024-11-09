import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2

mobilenet = mobilenet_v2(pretrained=True)
mobilenet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def generate_image_embedding(image):
    input_image = transform(image).unsqueeze(0)
    with torch.no_grad():
        embedding = mobilenet.features(input_image)
        return torch.flatten(embedding, 1).numpy()
