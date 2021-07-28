# vip-retrieval-demo

![](vip-retrieval.mp4)


--- OUTDATED --
# Setup
* Create and activate virtualenv for backend in `venv`:
  * `python -m venv venv`
  * `source venv/bin/activate`
* Install packages: `pip install -r requirements.txt` (if an error occurs, re-run the command)

## Detection Model

Python code in `api/detection` is taken from `vip-deepfashion` and slightly modified.
Model weights must downloaded from `https://speicherwolke.uni-leipzig.de/index.php/s/4WnNkGHn5rjzqc3` and copied to `api/detection/detection_weights.pkl`.

Test detection api: `curl -F file=@test.jpg  http://localhost:5000/api/detect`

## Embedding Model

Python code in `api/match` is taken from `vip-deepfashion` and slightly modified.
Model weights must be downloaded from: `https://speicherwolke.uni-leipzig.de/index.php/s/DjRj2KKRbQ9eZZb` and copied to `api/match/embedding_weights.pkl`
The model is used to create the embedding of an uploaded picture.
To compare the embedding with the database of products, annoy is used. The creation of the annoy index and a mapping from embeddings to products is done while converting the DeepFashion catalog to products.

Test matching: `curl -v POST http://localhost:5000/api/match -d @test_match.json --header "Content-Type: application/json"` (`image` value in `test_match_json` must be filled with response from detection api).

## Convert DeepFashion2 Dataset into product catalog
* Download and unzip `train.zip` from https://github.com/switchablenorms/DeepFashion2 into `deepfashion-raw` (PW: 2019Deepfashion2**)
* Download dataset of all short sleeve top fashion items and their embeddings from https://speicherwolke.uni-leipzig.de/index.php/s/SGACSd5wtd7rmGb and copy to: `embeddings/short_sleeve_top_train_embeddings.json`
* (Activate virtualenv)
* Run `python api/db_setup.py --deepfashion_embeddings=embeddings/short_sleeve_top_train_embeddings.json` to create product database and annoy index
* Move images: `mv deepfashion-raw/train/image  api/static/product-images/`
* Delete `rm -r deepfashion-raw`



## Setup frontend
* `npm install` from frontend directory to install all npm packages
* `npm run build` from frontend directory to build the frontend

([frontend readme](frontend/README.md))

# Run
* `npm run dev` for running the frontend
* `python api/api-start.py` for the api from project root directory
