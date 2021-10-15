import argparse
import os
import random
from pathlib import Path


def main(val_fraction: float, raw_data: str, output_path: str, seed: int = 42) -> None:
    """
    Splits the Deepfashion2 Dataset into train, valdiation and test set.
    This is necessary, since the test set is no provided.
    * We use the original validation set as our test set
    * And take a fraction of the training data (specified by val_fraction) as our validation set
    * The remaining training data is our training set
    :param val_fraction: fraction of train data that is used for validation
    :param raw_data: path to the deepfashion raw directory
    :param output_path: path were the final image lists are stored
    :param seed: random seed
    """
    print(val_fraction)
    print(raw_data)

    assert(0 <= val_fraction <= 1.0)
    assert(os.path.exists(raw_data))
    Path(output_path).mkdir(parents=True, exist_ok=True)

    source_directories = {'train': os.path.join(raw_data, 'train', 'image'),
                   'validation' : os.path.join(raw_data, 'train', 'image'),
                   'test': os.path.join(raw_data, 'validation', 'image')}
    images = {'train': os.listdir(source_directories['train']),
              'test': os.listdir(source_directories['test'])}

    # split
    random.seed(seed)
    random.shuffle(images['train'])  # random shuffle of the list
    images['validation'] = images['train'][0:int(len(images['train']) * val_fraction)]  # extract the first few elements of the list
    images['train'] = images['train'][int(len(images['train']) * val_fraction) + 1:]  # extract the last few elements of the list

    for split in ['train', 'test', 'validation']:
        with open(os.path.join(output_path, f'{split}_list.txt'), 'w') as f:
            for image in images[split]:
                f.write(f'{os.path.join(source_directories[split], image)}\n')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Create dataset splits for Deepfashion2')
    arg_parser.add_argument('-val-fraction',
                            help='Ratio of splitting train set in train and val',
                            default=0.2,
                            type=float)
    arg_parser.add_argument('--raw-data',
                            help='Path to raw df data',
                            default='data/raw',
                            type=str)
    arg_parser.add_argument('--output-path',
                            help='Path to output directory',
                            default='data/processed/detection',
                            type=str)
    args = arg_parser.parse_args()

    main(args.val_fraction, args.raw_data, args.output_path)
