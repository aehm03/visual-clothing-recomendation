import os

from detection.model import SSD300
from detection.utils import *
from torchvision import transforms

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
checkpoint = os.path.abspath('detection/detection_weights.pkl')

# create model as in training because I only saved the state_dict
model = SSD300(n_classes=14)
model = torch.nn.DataParallel(model)

# Load model checkpoint that is to be evaluated
model.load_state_dict(torch.load(checkpoint, map_location=device))
# Switch to eval mode
model.eval()

# Transforms
resize = transforms.Resize((300, 300))
to_tensor = transforms.ToTensor()
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])


def detect(original_image, min_score=0.2, max_overlap=0.5, top_k=200):
    """
    Detect objects in an image with a trained SSD300, and return the results
    :param original_image: image, a PIL Image
    :param min_score: minimum threshold for a detected box to be considered a match for a certain class
    :param max_overlap: maximum overlap two boxes can have so that the one with the lower score is not suppressed via Non-Maximum Suppression (NMS)
    :param top_k: if there are a lot of resulting detection across all classes, keep only the top 'k'
    :return: list of boxes and
    """

    # Transform
    original_image = original_image.convert('RGB')
    image = normalize(to_tensor(resize(original_image)))

    # Move to default device
    image = image.to(device)

    # Forward prop.
    predicted_locs, predicted_scores = model(image.unsqueeze(0))

    # Detect objects in SSD output
    det_boxes, det_labels, det_scores = model.module.detect_objects(predicted_locs, predicted_scores,
                                                                    min_score=min_score,
                                                                    max_overlap=max_overlap, top_k=top_k)

    # Move detections to the CPU
    det_boxes = det_boxes[0].to('cpu')

    # Transform to original image dimensions
    original_dims = torch.FloatTensor(
        [original_image.width, original_image.height, original_image.width, original_image.height]).unsqueeze(0)
    det_boxes = (det_boxes * original_dims).tolist()

    # Decode class integer labels
    det_labels = [rev_label_map[l] for l in det_labels[0].to('cpu').tolist()]

    # If no objects found, the detected labels will be set to ['0.'], i.e. ['background'] in SSD300.detect_objects()
    # in model.py
    if det_labels == ['background']:
        # Just return original image
        return []

    return [{'category': x, 'box': y} for x, y in zip(det_labels, det_boxes)]
