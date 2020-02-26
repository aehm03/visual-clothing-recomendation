# configuration
from api import db


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    images = db.Column(db.String)

    def __repr__(self):
        return 'Product ID: {},  Images: {}'.format(self.product_id, self.images)
