# vip-retrieval-demo

test api with curl: `curl -F file=@test.jpg  http://localhost:5000/api/detect`

<<<<<<< HEAD
# Setup
* Create and activate virtualenv for backend in `api/.venv`
=======

# Setup
* Create and activate virtualenv for backend in `.venv`

>>>>>>> 1ec3bf1f3b4c4881529c7f564ad04dba075b6f50
## Convert DeepFashion2 Dataset into product catalog
* Download and unzip `train.zip` from https://github.com/switchablenorms/DeepFashion2 into `deepfashion-raw`
* (Activate virtualenv)
* Run `python api/db_setup.py --deepfashion_annos=deepfashion-raw/train/annos` to create product database
<<<<<<< HEAD
* Move images: `mv deepfashion/raw/train/images  api/static/product-images/`
* Delete `rm -r deepfashion-raw
=======
* Move images: `mv deepfashion-raw/train/image  api/static/product-images/`
* Delete `rm -r deepfashion-raw`


## Setup frontend

Run `npm run build` from frontend directory to build the frontend
>>>>>>> 1ec3bf1f3b4c4881529c7f564ad04dba075b6f50
