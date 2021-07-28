import os
import pickle

import torch
from annoy import AnnoyIndex
from torchvision import transforms, models

# initialize model to create embeddings
img_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = models.resnet50(pretrained=True)
model.to(device)
model.eval()

# initialize index to retrieve nearest embeddings
u = AnnoyIndex(1000, 'euclidean')
u.load(os.path.join(os.path.dirname(__file__), 'embeddings.ann'))
embedding_to_product = {}
with open(os.path.join(os.path.dirname(__file__), 'embedding_to_product.pickle'), 'rb') as file:
    embedding_to_product = pickle.load(file)


def match_products(image, n_matches=5):
    image = image.convert('RGB')
    vec = img_transforms(image).to(device).unsqueeze(0)
    embedding = model.forward(vec).detach().squeeze().cpu().numpy()

    nearest = u.get_nns_by_vector(embedding, n=n_matches)
    print(nearest)
    return nearest

