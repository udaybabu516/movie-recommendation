# model/

This folder is intentionally kept empty (aside from this file).

This project uses a lightweight **content-based filtering** approach
(TF-IDF + Cosine Similarity) that is computed on the fly, in memory,
when the Flask app starts (see `recommender.py`). Because of this,
there is no pre-trained machine learning model file that needs to be
saved to disk.

This folder is kept in the project structure in case you want to
extend the project later — for example, saving a trained TF-IDF
vectorizer with `joblib`/`pickle` so it doesn't need to be rebuilt on
every server restart, or storing a more advanced model (such as a
collaborative-filtering matrix factorization model).
