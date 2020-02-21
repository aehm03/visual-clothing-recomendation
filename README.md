# vip-retrieval-demo

test api with curl: `curl -F file=@test.jpg  http://localhost:5000/api/detect`

# Setup
* Create and activate virtualenv for backend in `api/.venv`
## Convert DeepFashion2 Dataset into product catalog
* Download and unzip `train.zip` from https://github.com/switchablenorms/DeepFashion2 into `deepfashion-raw`
* (Activate virtualenv)
* Run `python api/db_setup.py --deepfashion_annos=deepfashion-raw/train/annos` to create product database
* Move images: `mv deepfashion/raw/train/images  api/static/product-images/`
* Delete `rm -r deepfashion-raw
