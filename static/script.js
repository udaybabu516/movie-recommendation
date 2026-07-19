/* ==========================================================
   CineMatch — Movie Recommendation System
   Frontend JavaScript: handles search, autocomplete, and
   rendering of recommendation results.
   ========================================================== */

// Grab references to all the DOM elements we need
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const suggestionsList = document.getElementById("suggestions");
const loader = document.getElementById("loader");
const errorBox = document.getElementById("errorBox");
const searchedMovieSection = document.getElementById("searchedMovieSection");
const searchedMovieCard = document.getElementById("searchedMovieCard");
const recommendationsSection = document.getElementById("recommendationsSection");
const recommendationsGrid = document.getElementById("recommendationsGrid");
const quickPicks = document.getElementById("quickPicks");
const languageFilters = document.getElementById("languageFilters");
const browseSection = document.getElementById("browseSection");
const browseGrid = document.getElementById("browseGrid");
const browseTitle = document.getElementById("browseTitle");

// A few example movies shown as clickable quick-pick buttons
// (a mix of English and Indian regional-language movies)
const EXAMPLE_MOVIES = ["Inception", "RRR", "Drishyam", "Vikram Vedha", "KGF: Chapter 2", "3 Idiots"];

// A small delay (debounce) so we don't call the API on every keystroke
let debounceTimer = null;

/* ---------------------------------------------------------
   Initial setup on page load
--------------------------------------------------------- */
function initQuickPicks() {
  EXAMPLE_MOVIES.forEach((title) => {
    const btn = document.createElement("button");
    btn.textContent = title;
    btn.addEventListener("click", () => {
      searchInput.value = title;
      fetchRecommendations(title);
    });
    quickPicks.appendChild(btn);
  });
}

/* ---------------------------------------------------------
   Language filters: "Browse by Language" chips
   (All, English, Hindi, Telugu, Tamil, Malayalam, Kannada...)
--------------------------------------------------------- */
async function initLanguageFilters() {
  try {
    const response = await fetch("/api/languages");
    const data = await response.json();

    // "All" is added manually as the first option
    const allLanguages = ["All", ...data.languages];

    allLanguages.forEach((lang, index) => {
      const chip = document.createElement("button");
      chip.className = "language-chip" + (index === 0 ? " active" : "");
      chip.textContent = lang;
      chip.addEventListener("click", () => {
        // Highlight the selected chip only
        document
          .querySelectorAll(".language-chip")
          .forEach((el) => el.classList.remove("active"));
        chip.classList.add("active");
        fetchBrowseByLanguage(lang);
      });
      languageFilters.appendChild(chip);
    });
  } catch (err) {
    console.error("Failed to load languages:", err);
  }
}

async function fetchBrowseByLanguage(language) {
  hideElement(errorBox);
  hideElement(searchedMovieSection);
  hideElement(recommendationsSection);

  try {
    const response = await fetch(`/api/browse?language=${encodeURIComponent(language)}`);
    const data = await response.json();
    renderBrowseGrid(data.movies, language);
  } catch (err) {
    console.error("Browse fetch error:", err);
  }
}

function renderBrowseGrid(movies, language) {
  browseGrid.innerHTML = "";
  browseTitle.textContent =
    language === "All" ? "Browsing All Movies" : `Browsing ${language} Movies`;

  movies.forEach((movie) => {
    const card = document.createElement("div");
    card.className = "movie-card";

    card.innerHTML = `
      <img src="${movie.poster_url}" alt="${escapeHtml(movie.title)} poster" />
      <div class="movie-card-body">
        <span class="badge lang-badge">${escapeHtml(movie.language)}</span>
        <h4>${escapeHtml(movie.title)}</h4>
        <div class="meta">${movie.release_year} &middot; ⭐ ${movie.rating}</div>
        <div class="meta">${escapeHtml(movie.genres)}</div>
      </div>
    `;

    // Clicking a browse card fetches recommendations for that movie
    card.addEventListener("click", () => {
      searchInput.value = movie.title;
      window.scrollTo({ top: 0, behavior: "smooth" });
      fetchRecommendations(movie.title);
    });

    browseGrid.appendChild(card);
  });

  showElement(browseSection);
}

/* ---------------------------------------------------------
   Autocomplete: fetch suggestions as the user types
--------------------------------------------------------- */
searchInput.addEventListener("input", () => {
  const query = searchInput.value.trim();

  clearTimeout(debounceTimer);

  if (query.length === 0) {
    suggestionsList.innerHTML = "";
    return;
  }

  // Wait 250ms after the user stops typing before calling the API
  debounceTimer = setTimeout(() => fetchSuggestions(query), 250);
});

async function fetchSuggestions(query) {
  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    renderSuggestions(data.results);
  } catch (err) {
    // Fail silently for autocomplete - not critical to the user experience
    console.error("Autocomplete error:", err);
  }
}

function renderSuggestions(titles) {
  suggestionsList.innerHTML = "";

  titles.forEach((title) => {
    const li = document.createElement("li");
    li.textContent = title;
    li.addEventListener("click", () => {
      searchInput.value = title;
      suggestionsList.innerHTML = "";
      fetchRecommendations(title);
    });
    suggestionsList.appendChild(li);
  });
}

// Hide suggestions when clicking elsewhere on the page
document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-box")) {
    suggestionsList.innerHTML = "";
  }
});

/* ---------------------------------------------------------
   Search button + Enter key trigger the main recommendation
--------------------------------------------------------- */
searchBtn.addEventListener("click", () => {
  const title = searchInput.value.trim();
  if (title) fetchRecommendations(title);
});

searchInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    const title = searchInput.value.trim();
    if (title) fetchRecommendations(title);
  }
});

/* ---------------------------------------------------------
   Fetch recommendations from the Flask backend
--------------------------------------------------------- */
async function fetchRecommendations(title) {
  // Reset UI state before starting a new search
  suggestionsList.innerHTML = "";
  hideElement(errorBox);
  hideElement(searchedMovieSection);
  hideElement(recommendationsSection);
  hideElement(browseSection);
  showElement(loader);

  try {
    const response = await fetch(`/api/recommend?title=${encodeURIComponent(title)}`);
    const data = await response.json();

    hideElement(loader);

    if (!response.ok) {
      // Handle invalid movie names gracefully with a friendly message
      showError(data.error || "Something went wrong. Please try again.");
      return;
    }

    renderSearchedMovie(data.searched_movie);
    renderRecommendations(data.recommendations);
  } catch (err) {
    hideElement(loader);
    showError("Could not connect to the server. Please make sure the app is running.");
    console.error("Recommendation fetch error:", err);
  }
}

/* ---------------------------------------------------------
   Rendering helpers
--------------------------------------------------------- */
function renderSearchedMovie(movie) {
  searchedMovieCard.innerHTML = `
    <img src="${movie.poster_url}" alt="${escapeHtml(movie.title)} poster" />
    <div class="movie-hero-info">
      <h3>${escapeHtml(movie.title)} (${movie.release_year})</h3>
      <div class="meta">
        <span class="badge rating-badge">⭐ ${movie.rating}</span>
        <span class="badge lang-badge">${escapeHtml(movie.language)}</span>
        ${movie.genres
          .split(" ")
          .map((g) => `<span class="badge">${escapeHtml(g)}</span>`)
          .join("")}
      </div>
      <p class="overview">${escapeHtml(movie.overview)}</p>
    </div>
  `;
  showElement(searchedMovieSection);
}

function renderRecommendations(movies) {
  recommendationsGrid.innerHTML = "";

  if (!movies || movies.length === 0) {
    recommendationsGrid.innerHTML = "<p>No similar movies found.</p>";
    showElement(recommendationsSection);
    return;
  }

  movies.forEach((movie) => {
    const card = document.createElement("div");
    card.className = "movie-card";

    const similarityPercent = Math.round(movie.similarity * 100);

    card.innerHTML = `
      <img src="${movie.poster_url}" alt="${escapeHtml(movie.title)} poster" />
      <div class="movie-card-body">
        <span class="badge lang-badge">${escapeHtml(movie.language)}</span>
        <h4>${escapeHtml(movie.title)}</h4>
        <div class="meta">${movie.release_year} &middot; ⭐ ${movie.rating}</div>
        <div class="meta">${escapeHtml(movie.genres)}</div>
        <div class="similarity-bar-track">
          <div class="similarity-bar-fill" style="width:${similarityPercent}%"></div>
        </div>
      </div>
    `;

    // Clicking a recommended movie searches for that movie next
    card.addEventListener("click", () => {
      searchInput.value = movie.title;
      window.scrollTo({ top: 0, behavior: "smooth" });
      fetchRecommendations(movie.title);
    });

    recommendationsGrid.appendChild(card);
  });

  showElement(recommendationsSection);
}

function showError(message) {
  errorBox.textContent = message;
  showElement(errorBox);
}

/* ---------------------------------------------------------
   Small utility functions
--------------------------------------------------------- */
function showElement(el) {
  el.classList.remove("hidden");
}

function hideElement(el) {
  el.classList.add("hidden");
}

// Basic HTML escaping to avoid rendering issues with special characters
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Initialize the quick pick buttons and language filter chips when the page loads
initQuickPicks();
initLanguageFilters();
