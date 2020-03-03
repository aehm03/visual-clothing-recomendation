# vip-retrieval-demo



# Setup
* Create and activate virtualenv for backend in `.venv`

## Convert DeepFashion2 Dataset into product catalog
* Download and unzip `train.zip` from https://github.com/switchablenorms/DeepFashion2 into `deepfashion-raw`
* (Activate virtualenv)
* Run `python api/db_setup.py --deepfashion_annos=deepfashion-raw/train/annos` to create product database
* Move images: `mv deepfashion-raw/train/image  api/static/product-images/`
* Delete `rm -r deepfashion-raw`

## Detection Model

Python code in `api/detection` is taken from `vip-deepfashion` anc slightly modified.
Model weights must downloaded from `https://speicherwolke.uni-leipzig.de/index.php/s/4WnNkGHn5rjzqc3` and copied to `api/detection/detection_weights.pkl`.

Test detection api: `curl -F file=@test.jpg  http://localhost:5000/api/detect`


## Setup frontend

Run `npm run build` from frontend directory to build the frontend
