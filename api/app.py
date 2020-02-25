import atexit
import os
import shutil
import tempfile
import uuid

from PIL import Image

from flask import Flask, Response, jsonify, request, abort, render_template, abort, url_for, send_from_directory


from flask_cors import CORS
from werkzeug.utils import secure_filename

# configuration
DEBUG = True
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = tempfile.mkdtemp()

# instantiate the app
app = Flask(__name__, static_folder="../frontend/dist/static", template_folder="../frontend/dist")
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# enable CORS
# TODO replace cors with other method for vue frontend
CORS(app, resources={r'/*': {'origins': '*'}})


# TODO which kind of data are the requests, form, json, wat?

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


products = {
    123: {
        'id': 123,
        'category': 'short sleeve top',
        'url': 'www.abc.de',
        'name': 'Product 123 Name'
    },
    456: {
        'id': 456,
        'category': 'short sleeve top',
        'url': 'www.abc.de',
        'name': 'Product 456 Name'
    }
}


@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Returns a single product identified by id
    :return:  { product: [(string)]}
    """
    if product_id not in products.keys():
        abort(404)
    return jsonify({'product': products.get(product_id)})


@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Routes the uploaded file URL's to the actual upload folder
    :param filename:
    :return:
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@atexit.register
def delete_files():
    """
    Cleans up the temporary upload-folder
    :return:
    """
    shutil.rmtree(app.config['UPLOAD_FOLDER'])


if __name__ == '__main__':
    app.run()
