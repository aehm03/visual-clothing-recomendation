# vip-retrieval-demo



# Setup
* Create and activate virtualenv for backend in `venv`

## Detection Model

Python code in `api/detection` is taken from `vip-deepfashion` and slightly modified.
Model weights must downloaded from `https://speicherwolke.uni-leipzig.de/index.php/s/4WnNkGHn5rjzqc3` and copied to `api/detection/detection_weights.pkl`.

Test detection api: `curl -F file=@test.jpg  http://localhost:5000/api/detect`

## Embedding Model

Python code in `api/match` is taken from `vip-deepfashion` and slightly modified.
Model weights must be downloaded from: `https://speicherwolke.uni-leipzig.de/index.php/s/DjRj2KKRbQ9eZZb` and copied to `api/match/embedding_weights.pkl`
The model is used to create the embedding of an uploaded picture.
To compare the embedding with the database of products, annoy is used. The creation of the annoy index and a mapping from embeddings to products is done while converting the DeepFashion catalog to products.

Test matching: `curl -v POST http://localhost:5000/api/match -d @test_match.json --header "Content-Type: application/json"` (image value must be filled with response from detection api).

## Convert DeepFashion2 Dataset into product catalog
* Download and unzip `train.zip` from https://drive.google.com/open?id=125F48fsMBz2EF0Cpqk6aaHet5VH399Ok into `deepfashion-raw`
* Download dataset of all short sleeve top fashion items and their embeddings from https://speicherwolke.uni-leipzig.de/index.php/s/HjSTBbmKzqaTx4X and copy to: `embeddings/short_sleeve_tops_training_embeddings.csv`
* (Activate virtualenv)
* Run `python api/db_setup.py --deepfashion_embeddings=embeddings/short_sleeve_tops_training_embeddings.csv` to create product database
* Move images: `mv deepfashion-raw/train/image  api/static/product-images/`
* Delete `rm -r deepfashion-raw` to become more light-weight?
TODO: why delete?


## Setup frontend
* Run `npm install` from frontend directory to install all npm packages
* Run `npm run build` from frontend directory to build the frontend
