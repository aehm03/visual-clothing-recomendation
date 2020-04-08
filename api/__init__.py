import tempfile

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../frontend/dist/static", template_folder="../frontend/dist")
app.config.from_object(__name__)

UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# enable CORS
# TODO replace cors with other method for vue frontend
CORS(app, resources={r'/*': {'origins': '*'}})

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
