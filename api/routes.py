import os
import uuid

from PIL import Image
from api import app
from api.detection.detection import detect
from flask import Response, abort, jsonify, request, render_template, url_for, send_from_directory
from api.match.match import match_products
from api.models import Product
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def frontend():
    """
    Serves the frontend of the application.
    :return: frontend index.html
    """
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/detect', methods=['POST'])
def detection():
    """
    detects objects categories and their position in the posted image.
    :return: list of detected objects and bounding boxes
    """
    if 'file' not in request.files:
        return Response('[DETECT]  no file part', status=400)

    file = request.files['file']

    # if user does not select file, browser may submit an empty part without filename
    if file.filename == '':
        return Response('[DETECT] empty file part', status=400)

    if not allowed_file(file.filename):
        return Response(file.filename + '[DETECT] is not in allowed extensions ' + ALLOWED_EXTENSIONS, status=400)

    filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.split('.')[-1])
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    img = Image.open(file.stream)
    url = url_for('uploaded_file', filename=filename)

    return jsonify({'image_url': url, 'items': detect(img)})


@app.route('/api/image/<string:image_id>', methods=['GET'])
def get_image(image_id):
    """
    returns a product image
    :param image_id:
    :return:
    """
    filename = secure_filename(image_id + '.jpg')
    return send_from_directory(app.config['PRODUCT_IMAGE_FOLDER'], filename)


@app.route('/api/match/categories')
def categories():
    """
    Returns all available product categories
    :return:  { categories: [(string)]}
    """
    return jsonify({'categories': [{'short sleeve top',
                                    'trousers',
                                    'short sleeve dress',
                                    'shorts',
                                    'sling dress',
                                    'sling',
                                    'long sleeve outwear',
                                    'long sleeve top',
                                    'skirt',
                                    'vest dress',
                                    'long sleeve dress',
                                    'vest',
                                    'short sleeve outwear'}]})


@app.route('/api/match', methods=['POST'])
def match():
    """
    Matches the given product with the catalog and returns up to 5 similar products.
    Request body must be of type json and contain
    - image: filename of previously uploaded image
    - category: not yet used
    optional:
    -b box: coordinates to crop the image
    :return: {'matches': [list of ids]]}
    """

    content = request.get_json()
    box = content['box']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], content['image'])

    try:
        img = Image.open(filename)
        if box is not None:
            img = Image.open(filename).crop(box)

        matches = match_products(img)
        return jsonify({'matches': matches})
    except FileNotFoundError:
        raise BadRequest()


@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Returns a single product identified by id
    :return:  { product: [(string)]}
    """
    p = Product.query.get(product_id)
    if p is None:
        abort(404)
    return jsonify({'product_id': p.product_id, 'category_id': p.category_id, 'images': [p.product_id],
                    'name': p.display_name, 'season': p.season, 'usage': p.usage,
                    'type': p.type, 'color': p.color})


@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Routes the uploaded file URL's to the actual upload folder
    :param filename:
    :return:
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
