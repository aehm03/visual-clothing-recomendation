import sys

sys.path.append('.')

import argparse
import json
import os
import re
from glob import glob

import pandas as pd
from . import app, db
from models import Product
from sqlalchemy_utils import create_database, database_exists
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--deepfashion_annos', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':

    print(app.config)

    args = parse_args()
    path = os.path.join(args.deepfashion_annos, '*.json')

    item_list = []
    for file_name in tqdm(glob(os.path.join(args.deepfashion_annos, '*.json'))):
        with open(file_name) as json_file:
            annotation = json.load(json_file)
            if annotation['source'] == 'shop':

                im_id = re.findall(r"\d+", file_name)[0]
                for key in annotation.keys():

                    if key.startswith('item'):
                        item = annotation[key]
                        item_list.append({'image_id': im_id, 'category_id': item['category_id'], 'style': item['style'],
                                          'pair_id': annotation['pair_id']})

    item_df = pd.DataFrame(item_list)

    # filter on short sleeve tops (category_id == 1)
    # items with style 0 have no match
    item_df = item_df.loc[(item_df['category_id'] == 1) & (item_df['style'] > 0)]

    # group by product
    products = item_df.groupby(['pair_id', 'category_id', 'style'])['image_id'].apply(','.join).reset_index()

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()

    # iterate over products and fill database
    for idx, row in products.iterrows():
        product = Product(product_id=idx, category_id=row['category_id'], images=row['image_id'])
        db.session.add(product)

    db.session.commit()
