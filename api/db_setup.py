import math
import os
import pickle
import sys

sys.path.append('.')

import argparse
from annoy import AnnoyIndex
import pandas as pd
from api import app, db
from api.models import Product
from sqlalchemy_utils import create_database, database_exists


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deepfashion_embeddings', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    item_df = pd.read_json(args.deepfashion_embeddings, orient='table')

    # filter on short sleeve tops (category_id == 1)
    # items with style 0 have no match
    item_df = item_df.loc[(item_df['category_id'] == 1) & (item_df['style'] > 0)]

    # group by product
    products = item_df.groupby(['item_group_id'])['image_id'].apply(','.join)

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
    embedding_index = AnnoyIndex(128, 'euclidean')
    embedding_index.on_disk_build(os.path.abspath('api/match/embeddings.ann'))
    embedding_to_product = {}
    for i, row in item_df.iterrows():
        embedding_index.add_item(i, row['embedding_vector'])
        embedding_to_product[i] = row['item_group_id']

    n_trees = 4 * int(math.sqrt(len(item_df)))
    embedding_index.build(n_trees)

    with open(os.path.abspath('api/match/embedding_to_product.pickle'), 'wb') as file:
        pickle.dump(embedding_to_product, file)
