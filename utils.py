"""
utils.py
--------
Small helper functions used by app.py. Kept separate from app.py so
that the main application file stays clean and focused on routing.

Currently this file handles fetching movie posters from the free
TMDb (The Movie Database) API. If no API key is configured, or if
the request fails for any reason, a placeholder poster image is
returned instead so the app never breaks.
"""

import os
import requests

# TMDb API configuration.
# To enable real posters:
#   1. Create a free account at https://www.themoviedb.org/
#   2. Get an API key from your account settings (API section)
#   3. Set it as an environment variable named TMDB_API_KEY
#      (see README.md for exact instructions)
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w342"

# A simple placeholder image shown when no poster can be found,
# or when no TMDb API key has been configured.
PLACEHOLDER_POSTER = "https://placehold.co/342x513?text=No+Poster"


def get_poster_url(movie_title, release_year=None):
    """
    Fetches a movie poster image URL from TMDb given a movie title.

    If the TMDB_API_KEY environment variable is not set, or if the
    request fails / no result is found, this function safely returns
    a placeholder image URL instead of raising an error.
    """
    # If no API key is configured, skip the network call entirely
    if not TMDB_API_KEY:
        return PLACEHOLDER_POSTER

    try:
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title,
        }
        if release_year:
            params["year"] = release_year

        # Give the request a short timeout so the app never hangs
        response = requests.get(TMDB_SEARCH_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return PLACEHOLDER_POSTER

        poster_path = results[0].get("poster_path")
        if not poster_path:
            return PLACEHOLDER_POSTER

        return TMDB_IMAGE_BASE_URL + poster_path

    except requests.RequestException:
        # Any network error, timeout, or bad response falls back
        # gracefully to the placeholder image.
        return PLACEHOLDER_POSTER
