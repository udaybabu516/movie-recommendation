"""
recommender.py
----------------
This file contains the core recommendation logic for the Movie
Recommendation System. It uses TF-IDF (Term Frequency-Inverse Document
Frequency) to convert movie text data (genres + overview) into numeric
vectors, and then uses Cosine Similarity to find movies that are most
similar to each other.

This is a "content-based" recommendation system, meaning it recommends
movies based on the content/description of the movies themselves,
not based on other users' ratings.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    """
    A simple content-based movie recommender system.

    Steps:
    1. Load movie data from a CSV file.
    2. Combine 'genres' and 'overview' into a single text field.
    3. Convert that text into TF-IDF vectors.
    4. Compute cosine similarity between all movies.
    5. Given a movie title, return the most similar movies.
    """

    def __init__(self, csv_path="movies.csv"):
        # Load the dataset into a pandas DataFrame
        self.movies_df = pd.read_csv(csv_path)

        # Clean up the data: make sure there are no missing values
        # in the columns we depend on for text analysis.
        self.movies_df["genres"] = self.movies_df["genres"].fillna("")
        self.movies_df["overview"] = self.movies_df["overview"].fillna("")
        self.movies_df["language"] = self.movies_df["language"].fillna("English")

        # Combine genres and overview into one "content" column.
        # We repeat the genres twice to give them slightly more weight,
        # since genre similarity is usually a strong signal for
        # "similar movies".
        self.movies_df["content"] = (
            self.movies_df["genres"] + " " +
            self.movies_df["genres"] + " " +
            self.movies_df["overview"]
        )

        # Build a lowercase title column for easy, case-insensitive search
        self.movies_df["title_lower"] = self.movies_df["title"].str.lower()

        # Build the TF-IDF matrix and similarity matrix once, when the
        # recommender is created, so we don't have to recompute it on
        # every single request (this keeps the app fast).
        self._build_similarity_matrix()

    def _build_similarity_matrix(self):
        """
        Converts movie text content into TF-IDF vectors and computes
        the cosine similarity between every pair of movies.
        """
        # TF-IDF turns text into numbers based on how important each
        # word is to a document relative to all other documents.
        # stop_words="english" removes common words like "the", "a", "is".
        tfidf = TfidfVectorizer(stop_words="english")

        # Fit the vectorizer on our combined content column and
        # transform it into a matrix of TF-IDF features.
        tfidf_matrix = tfidf.fit_transform(self.movies_df["content"])

        # Cosine similarity measures the angle between two vectors.
        # A value of 1 means the movies are identical in content,
        # 0 means they share nothing in common.
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def search_movies(self, query, limit=8):
        """
        Search for movies whose title contains the given query string.
        Used for the autocomplete/search feature on the frontend.

        Returns a list of matching titles (strings).
        """
        query = query.strip().lower()
        if not query:
            return []

        # Find all titles that contain the search query
        matches = self.movies_df[
            self.movies_df["title_lower"].str.contains(query, na=False)
        ]

        return matches["title"].head(limit).tolist()

    def get_movie_details(self, title):
        """
        Return a dictionary of details for a single movie by exact title.
        Returns None if the movie is not found.
        """
        row = self.movies_df[self.movies_df["title_lower"] == title.strip().lower()]

        if row.empty:
            return None

        row = row.iloc[0]
        return {
            "title": row["title"],
            "genres": row["genres"],
            "overview": row["overview"],
            "release_year": int(row["release_year"]),
            "rating": float(row["rating"]),
            "language": row["language"],
        }

    def get_recommendations(self, title, top_n=6):
        """
        Given a movie title, return a list of the top_n most similar
        movies (excluding the movie itself).

        Returns None if the movie title is not found in the dataset.
        """
        title_lower = title.strip().lower()

        # Check if the movie exists in our dataset
        if title_lower not in self.movies_df["title_lower"].values:
            return None

        # Find the index (row number) of the movie the user searched for
        movie_index = self.movies_df[
            self.movies_df["title_lower"] == title_lower
        ].index[0]

        # Get the similarity scores of this movie with every other movie
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))

        # Sort movies by similarity score, highest first
        similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1], reverse=True
        )

        # Skip the first result because it will always be the movie itself
        # (similarity of a movie with itself is always 1.0)
        top_matches = similarity_scores[1:top_n + 1]

        # Build a list of recommended movie details
        recommendations = []
        for index, score in top_matches:
            movie_row = self.movies_df.iloc[index]
            recommendations.append({
                "title": movie_row["title"],
                "genres": movie_row["genres"],
                "overview": movie_row["overview"],
                "release_year": int(movie_row["release_year"]),
                "rating": float(movie_row["rating"]),
                "language": movie_row["language"],
                "similarity": round(float(score), 3),
            })

        return recommendations

    def get_all_titles(self):
        """Return a list of every movie title in the dataset (used for
        showing a default/full movie list on the homepage)."""
        return self.movies_df["title"].tolist()

    def get_languages(self):
        """
        Return a sorted list of every unique language present in the
        dataset (e.g. English, Hindi, Telugu, Tamil, Malayalam, Kannada).
        Used to build the "Browse by Language" filter on the frontend.
        """
        return sorted(self.movies_df["language"].unique().tolist())

    def get_movies_by_language(self, language, limit=60):
        """
        Return a list of movie summaries for a given language, sorted
        by rating (highest first). If language is "All", every movie
        in the dataset is returned.
        """
        if language.lower() == "all":
            filtered = self.movies_df
        else:
            filtered = self.movies_df[
                self.movies_df["language"].str.lower() == language.strip().lower()
            ]

        filtered = filtered.sort_values(by="rating", ascending=False).head(limit)

        movies = []
        for _, row in filtered.iterrows():
            movies.append({
                "title": row["title"],
                "genres": row["genres"],
                "release_year": int(row["release_year"]),
                "rating": float(row["rating"]),
                "language": row["language"],
            })
        return movies
