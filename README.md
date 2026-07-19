# 🎬 CineMatch — Movie Recommendation System

A simple, clean, and beginner-friendly **content-based Movie Recommendation System** built with Python, Flask, Pandas, and Scikit-learn. It uses **TF-IDF vectorization** and **Cosine Similarity** to recommend movies similar to one you search for.

---

## 📖 Project Overview

CineMatch lets you search for a movie you like, and instantly recommends similar movies based on genre and plot overview similarity — no user ratings or complex machine learning required. It's a great starting project for learning how content-based recommendation engines work.

The dataset includes **133 movies** spanning **English, Hindi, Telugu, Tamil, Malayalam, Kannada, and Korean** cinema, so you can search and get recommendations across Hollywood and Indian regional films alike.

The recommendation logic works like this:
1. Every movie's **genres + overview** are combined into one text field.
2. That text is converted into numeric vectors using **TF-IDF** (Term Frequency–Inverse Document Frequency).
3. **Cosine Similarity** is calculated between every pair of movies.
4. When you search a movie, the app returns the movies with the highest similarity score.

---

## ✨ Features

- 🔍 Search movies by title (with live autocomplete suggestions)
- 🎯 Get top 6 similar movie recommendations instantly
- 🌐 **133 movies** across **English, Hindi, Telugu, Tamil, Malayalam, Kannada, and Korean** cinema
- 🗂️ **Browse by Language** filter chips — jump straight into Telugu, Tamil, Malayalam, Kannada, or Hindi movie lists
- 🖼️ Movie posters via the free **TMDb API** (optional — falls back to a placeholder if no API key is set)
- 🎭 Displays title, genre(s), overview, release year, rating, and language
- ⚠️ Handles invalid/unknown movie names gracefully with a friendly error message
- 📱 Fully responsive UI — works on desktop, tablet, and mobile
- ⚡ Fast — the similarity matrix is built once at server startup
- 🧩 Clean, well-commented, beginner-friendly code (no complex architecture)

---

## 📁 Folder Structure

```
Movie-Recommendation-System/
│
├── app.py                # Flask backend — routes & API endpoints
├── recommender.py        # TF-IDF + Cosine Similarity recommendation logic
├── utils.py               # Helper functions (TMDb poster fetching)
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── movies.csv             # Sample dataset (55 movies)
│
├── templates/
│   └── index.html         # Main HTML page
│
├── static/
│   ├── style.css           # Modern, responsive styling
│   └── script.js           # Frontend logic (search, autocomplete, rendering)
│
└── model/
    └── README.md           # Notes on why no saved model file is needed
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher installed on your machine
- `pip` (comes with Python)

### 1. Download / Clone the Project
Place the `Movie-Recommendation-System` folder anywhere on your computer, then open a terminal inside it.

### 2. Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from other Python projects on your system.

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked when you see `(venv)` at the start of your terminal prompt.

### 3. Install Dependencies

With your virtual environment activated, run:

```
pip install -r requirements.txt
```

This installs Flask, Pandas, NumPy, Scikit-learn, and Requests.

### 4. (Optional) Enable Real Movie Posters with TMDb

By default, the app shows a placeholder poster image for every movie. To show **real posters**:

1. Create a free account at [themoviedb.org](https://www.themoviedb.org/)
2. Go to **Settings → API** and request a free API key
3. Set it as an environment variable before running the app:

**Windows (Command Prompt):**
```
set TMDB_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```
$env:TMDB_API_KEY="your_api_key_here"
```

**macOS / Linux:**
```
export TMDB_API_KEY=your_api_key_here
```

This step is completely optional — the app works fully without it, just with placeholder poster images.

### 5. Run the Application

**Windows:**
```
python app.py
```

**macOS / Linux:**
```
python3 app.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000
```

### 6. Open in Browser

Go to: **http://127.0.0.1:5000**

---

## 🧪 Example Usage

1. Open the app in your browser.
2. Type a movie name into the search box, e.g. `Inception`.
3. Either click a suggestion from the dropdown, click **Search**, or press **Enter**.
4. You'll see:
   - The details of the movie you searched for (poster, genre, overview, year, rating)
   - A grid of the top 6 most similar movies, each with a similarity bar
5. Click on any recommended movie card to search for that movie next and explore further.

Try searching for: `The Godfather`, `RRR`, `Drishyam`, `Vikram Vedha`, `KGF: Chapter 2`, or `3 Idiots`.

You can also click the **language filter chips** (All, English, Hindi, Telugu, Tamil, Malayalam, Kannada, Korean) below the search box to browse top-rated movies in that language without typing anything — then click any movie card to see its recommendations.

---

## 🧯 Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`. |
| `python` command not found | Try `python3` instead of `python` (common on macOS/Linux). |
| Page loads but posters don't show real images | This is expected without a TMDb API key — see step 4 above. Placeholder images are shown instead, and the app still works fully. |
| `Address already in use` / port 5000 busy | Another program is using port 5000. Stop it, or edit the last line of `app.py` to use a different port, e.g. `app.run(debug=True, port=5001)`. |
| Movie search returns "not found" | Make sure the title matches one in `movies.csv` — use the autocomplete dropdown to pick an exact match. |
| CSS/JS not loading (page looks unstyled) | Make sure you're running the app via `python app.py` and opening `http://127.0.0.1:5000`, not opening `index.html` directly as a file. |

---

## 🚀 Future Improvements

- Add more movies to `movies.csv` (or connect to a live movie database)
- Add collaborative filtering based on user ratings, in addition to content-based filtering
- Add filtering by genre or release year on the frontend
- Add a "favorites" list saved locally
- Add pagination for browsing the full movie catalog
- Cache TMDb poster results to reduce repeated API calls
- Deploy the app online (e.g., Render, Railway, PythonAnywhere)

---

## 🧰 Tech Stack

- **Backend:** Python, Flask
- **Data Handling:** Pandas, NumPy
- **Recommendation Engine:** Scikit-learn (TF-IDF + Cosine Similarity)
- **Posters:** TMDb API (free, optional)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no frameworks needed)

---

Enjoy discovering your next favorite movie! 🍿
