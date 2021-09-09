import math
import os
import sys

sys.path.append('.')

import argparse
import pickle
from annoy import AnnoyIndex
from api import app, db
from api.models import Product
from sqlalchemy_utils import create_database, database_exists


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fashion-dataset', type=str, required=True)
    return parser.parse_args()


def create_product_db(dataset_path):

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    db.drop_all()
    db.create_all()

    with open(os.path.join(dataset_path, 'styles.csv')) as f:
        for line in f.readlines():
            obj = [item.strip() for item in line.split(',')]
            if obj[0].isdigit():
                product = Product(product_id=int(obj[0]),
                                  category_id=0,
                                  display_name=obj[-1],
                                  season=obj[-4],
                                  usage=obj[-2],
                                  color=obj[-5],
                                  type=obj[-6])
                db.session.add(product)

    db.session.commit()


def create_index(dataset_path):
    with open(os.path.join(dataset_path, 'embeddings.csv')) as f:

        # create index for matching
        embedding_index = AnnoyIndex(1000, 'euclidean')
        embedding_index.on_disk_build(os.path.abspath('api/match/embeddings.ann'))

        embedding_to_product = {}

        # skip header
        f.readline()
        size = 0
        for line in f.readlines():
            obj = line.split(',')
            embedding_index.add_item(size, [float(i) for i in obj[1:]])
            embedding_to_product[size] = int(obj[0])
            size += 1

    # magic to compute optimal number of trees in ANNOY indez
    n_trees = 4 * int(math.sqrt(size))
    embedding_index.build(n_trees)
    with open('api/match/embedding_to_product.pickle', 'wb') as file:
        pickle.dump(embedding_to_product, file)


def main(dataset_path):
    create_product_db(dataset_path)
    #create_index(dataset_path)


if __name__ == '__main__':
    args = parse_args()
    main(args.fashion_dataset)

