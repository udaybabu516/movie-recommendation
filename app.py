"""
app.py
------
Main Flask application file for the Movie Recommendation System.

Routes:
    GET  /                 -> Renders the homepage (search UI)
    GET  /api/search       -> Returns movie titles matching a search query
                               (used for autocomplete suggestions)
    GET  /api/recommend    -> Returns movie details + recommended movies
                               for a given movie title
    GET  /api/all-movies   -> Returns the full list of movie titles

Run this file with: python app.py
"""

from flask import Flask, render_template, request, jsonify

from recommender import MovieRecommender
from utils import get_poster_url

# Create the Flask application
app = Flask(__name__)

# Load and prepare the recommender system once when the server starts.
# Building the TF-IDF/similarity matrix is a bit of work, so we do it
# a single time here instead of on every request.
recommender = MovieRecommender(csv_path="movies.csv")


@app.route("/")
def home():
    """Render the main page of the app."""
    return render_template("index.html")


@app.route("/api/search")
def search_movies():
    """
    Search endpoint used for autocomplete suggestions.
    Example: /api/search?q=dark
    """
    query = request.args.get("q", "")
    matches = recommender.search_movies(query)
    return jsonify({"results": matches})


@app.route("/api/all-movies")
def all_movies():
    """Return every movie title, used to populate a 'browse all' list."""
    return jsonify({"titles": recommender.get_all_titles()})


@app.route("/api/languages")
def languages():
    """Return every unique language available in the dataset, used to
    build the 'Browse by Language' filter chips on the frontend."""
    return jsonify({"languages": recommender.get_languages()})


@app.route("/api/browse")
def browse():
    """
    Return a list of movies for a given language, so users can browse
    Telugu, Tamil, Malayalam, Kannada, Hindi, or English movies without
    needing to search for a specific title first.
    Example: /api/browse?language=Telugu
    """
    language = request.args.get("language", "All")
    movies = recommender.get_movies_by_language(language)

    # Attach poster URLs to each movie in the browse results
    for movie in movies:
        movie["poster_url"] = get_poster_url(movie["title"], movie["release_year"])

    return jsonify({"language": language, "movies": movies})


@app.route("/api/recommend")
def recommend():
    """
    Main recommendation endpoint.
    Example: /api/recommend?title=Inception

    Returns:
        - The searched movie's own details (with poster)
        - A list of recommended similar movies (each with poster)
        - An error message if the movie is not found
    """
    title = request.args.get("title", "").strip()

    # Handle empty input gracefully
    if not title:
        return jsonify({"error": "Please provide a movie title."}), 400

    # Look up the searched movie's details first
    movie_details = recommender.get_movie_details(title)

    if movie_details is None:
        # Movie not found in our dataset - handle gracefully with a
        # helpful error message instead of crashing.
        return jsonify({
            "error": f"Sorry, '{title}' was not found in our movie database. "
                     f"Please check the spelling or try another movie."
        }), 404

    # Attach a poster URL to the searched movie
    movie_details["poster_url"] = get_poster_url(
        movie_details["title"], movie_details["release_year"]
    )

    # Get similar movie recommendations
    recommendations = recommender.get_recommendations(title, top_n=6)

    # Attach a poster URL to each recommended movie
    for movie in recommendations:
        movie["poster_url"] = get_poster_url(
            movie["title"], movie["release_year"]
        )

    return jsonify({
        "searched_movie": movie_details,
        "recommendations": recommendations,
    })


if __name__ == "__main__":
    # debug=True auto-reloads the server on code changes (development only)
    app.run(debug=True, host="0.0.0.0", port=5000)
