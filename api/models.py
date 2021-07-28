# configuration
from api import db


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    display_name = db.Column(db.String)
    season = db.Column(db.String)
    usage = db.Column(db.String)
    type = db.Column(db.String)
    color = db.Column(db.String)

    def __repr__(self):
        return 'Product ID: {},  Name: {}'.format(self.product_id, self.display_name)
