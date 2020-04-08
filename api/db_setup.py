import os
import pickle
import sys

sys.path.append('.')

import argparse
from annoy import AnnoyIndex
import pandas as pd
from api import app, db
from models import Product
from sqlalchemy_utils import create_database, database_exists


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deepfashion_embeddings', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    item_df = pd.read_csv(args.deepfashion_embeddings, dtype={'image_id': object})

    # filter on short sleeve tops (category_id == 1)
    # items with style 0 have no match
    item_df = item_df.loc[(item_df['category_id'] == 1) & (item_df['style'] > 0)]

    # group by product
    products = item_df.groupby(['group_id'])['image_id'].apply(','.join)

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.drop_all()
    db.create_all()

    # iterate over products and fill database
    for group_id, image_id in products.iteritems():
        product = Product(product_id=group_id, category_id=1, images=image_id)
        db.session.add(product)

    db.session.commit()

    # create index for matching
    embedding_index = AnnoyIndex(128, 'angular')
    embedding_index.on_disk_build(os.path.abspath('api/match/embeddings.ann'))
    for i, row in item_df.iterrows():
        embedding_index.add_item(i, row[4:132].array)
    embedding_index.build(10)
    # create dict embedding_id -> product_id
    embedding_to_product = item_df['group_id'].to_dict()
    with open(os.path.abspath('api/match/embedding_to_product.pickle'), 'wb') as file:
        pickle.dump(embedding_to_product, file)
