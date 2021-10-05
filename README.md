# Visual Clothing Recommendation
Fashion item identification and recommendation API for the [VIP](https://infai.org/vip/) project.

The detection API takes an images an returns segments of the image along with a class. 
The match API takes such segments (or any other image for that matter) and returns similar items from a database. 
Different front-ends (touch screen mirror or web app) can be used.


![](vip-retrieval.mp4)

Test detection api: `curl -F file=@test.jpg  http://localhost:5000/api/detect`
Test matching: `curl -v POST http://localhost:5000/api/match -d @test_match.json --header "Content-Type: application/json"` (`image` value in `test_match_json` must be filled with response from detection api).

## Components
The system consists of a detection model, an embedding model (to create an embedding vector of the uploaded picture), a database of 'store' items and an nearest neighbor index to compute the most similar database items for a given query image.

### Detection Model

Python code in `api/detection` is taken from `vip-deepfashion` and slightly modified.
Model weights must be copied to `api/detection/detection_weights.pkl`.



### Embedding Model

Python code in `api/match` is taken from `vip-deepfashion` and slightly modified.
Model weights must be copied to `api/match/embedding_weights.pkl`
The model is used to create the embedding of an uploaded picture.
Also each of the database images must be converted into an once embedding for similarity matching.

### Database
Just an SQLite database, see `db_setup.py`

### Nearest Neighbor Retrieval
To compare the embedding with the database of products, [ANNOY](https://github.com/spotify/annoy) is used. The creation of the annoy index and a mapping from embeddings to products is done while setting up the database.

# Setup

TODO

# Run
* `python api/api-start.py` 

# Further Ideas

# Related Work
* https://github.com/flipkart-incubator/fk-visual-search
