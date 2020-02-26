import os
import uuid

from PIL import Image
from api import app
from flask import Response, abort, jsonify, request, render_template, url_for, send_from_directory
from models import Product
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

    # Currently we return a box that covers the whole image and contains a short_sleeve_top
    return jsonify({'image_url': url, 'items': [{'category': 'short sleeve top', 'box': [0, 0, *img.size]}]})


@app.route('/api/match/categories')
def categories():
    """
    Returns all available product categories
    TODO matching only works with "short sleeve tops"s!
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
    Matches the given product with the catalog and returns n similar products
    :return:
    """

    return jsonify({'matches': [{'id': 123}, {'id': 456}]})


@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Returns a single product identified by id
    :return:  { product: [(string)]}
    """
    p = Product.query.get(product_id)
    if p is None:
        abort(404)
    return jsonify({'product_id': p.product_id, 'category_id': p.category_id, 'images': p.images.split(',')})


@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Routes the uploaded file URL's to the actual upload folder
    :param filename:
    :return:
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
