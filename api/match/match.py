import os
import pickle

import torch
from annoy import AnnoyIndex
from match.model import EmbedNetwork
from torch import nn
from torchvision import transforms

# initialize model to create embeddings
img_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
checkpoint = os.path.join(os.path.dirname(__file__), 'embedding_weights.pkl')
model = EmbedNetwork()
model = nn.DataParallel(model)
model.load_state_dict(torch.load(checkpoint, map_location=device))
model.eval()

# initialize index to retrieve nearest embeddings
u = AnnoyIndex(128, 'angular')
u.load(os.path.join(os.path.dirname(__file__), 'embeddings.ann'))
embedding_to_product = {}
with open(os.path.join(os.path.dirname(__file__), 'embedding_to_product.pickle'), 'rb') as file:
    embedding_to_product = pickle.load(file)


def match_products(image, n_matches=5):
    image = image.convert('RGB')
    vec = img_transforms(image)

    # Move to default device
    vec = vec.to(device)

    embedding = model(vec.unsqueeze(0))
    embedding = embedding.cpu().detach().numpy()[0]

    # this is a bit hacky, we can not gurantee to get n nearest products by looking for n nearest embeddings
    # bc products have more than one image/embedding
    # we take n*three, map to product unique id and truncate at n
    # could still be less than n
    nearest = u.get_nns_by_vector(embedding, n=n_matches * 3)
    return [x for i, x in enumerate(nearest) if nearest.index(x) == i][0:n_matches]
