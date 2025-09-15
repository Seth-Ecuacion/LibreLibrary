import streamlit as st
import requests

st.set_page_config(page_title="LibreLibrary", page_icon="📚", layout="wide")
st.title("📚 Welcome to LibreLibrary")

# CSS for book cards
st.markdown("""
<style>
.book-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    width: 220px;
    height: 450px;
    text-align: center;
    margin: 10px auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
    overflow: hidden;
}
.book-card:hover {
    transform: scale(1.05);
    box-shadow: 4px 4px 12px rgba(0,0,0,0.2);
}
.book-cover-container {
    width: 100%;
    height: 260px;
    overflow: hidden;
    border-radius: 5px;
    margin-bottom: 10px;
}
.book-cover-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;  /* Ensures consistent image sizing */
}
.truncate {
    display: block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)

# Helper to truncate text
def truncate_text(text, max_length=30):
    return text[:max_length] + "..." if len(text) > max_length else text

# Function to create a single book card
def create_book_card(book, key_prefix):
    title = truncate_text(book.get("title", "Unknown Title"), 30)
    authors = truncate_text(", ".join(book.get("author_name", ["Unknown Author"])), 30)
    year = book.get("first_publish_year", "N/A")
    cover_id = book.get("cover_i")
    work_key = book.get("key", "")

    # Fallback placeholder if no cover
    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "https://via.placeholder.com/220x260?text=No+Cover"

    # Display card
    st.markdown(f"""
        <div class="book-card">
            <div class="book-cover-container">
                <img src="{cover_url}" />
            </div>
            <b class="truncate">{title}</b><br>
            <small class="truncate">👤 {authors}<br>📅 {year}</small>
        </div>
    """, unsafe_allow_html=True)

    # Buttons
    st.button("🔍 Details", key=f"{key_prefix}_details")
    st.button("📖 Read", key=f"{key_prefix}_read")
    st.button("⬇️ Download", key=f"{key_prefix}_download")

# Function to fetch books from Open Library
def fetch_books(query, max_results=9):
    url = f"https://openlibrary.org/search.json?q={query}&limit={max_results}"
    response = requests.get(url).json()
    return response.get("docs", [])

# Carousel for books
def create_carousel(books, books_per_page=5, carousel_name="main"):
    if f"{carousel_name}_index" not in st.session_state:
        st.session_state[f"{carousel_name}_index"] = 0

    start = st.session_state[f"{carousel_name}_index"]
    end = start + books_per_page
    display_books = books[start:end]

    cols = st.columns(len(display_books))
    for col, book in zip(cols, display_books):
        with col:
            create_book_card(book, key_prefix=f"{book.get('key','')}_{start}")

    # Navigation buttons
    prev_col, next_col = st.columns([1,1])
    with prev_col:
        if st.button(f"⬅️ Previous", key=f"{carousel_name}_prev") and start > 0:
            st.session_state[f"{carousel_name}_index"] -= books_per_page
            # No rerun call needed, button click triggers rerun automatically
    with next_col:
        if st.button(f"Next ➡️", key=f"{carousel_name}_next") and end < len(books):
            st.session_state[f"{carousel_name}_index"] += books_per_page

# ---------------------------
# Example usage
# ---------------------------
query = st.text_input("🔍 Search for a book")

if query:
    with st.spinner("Searching books..."):
        results = fetch_books(query)
        create_carousel(results, books_per_page=3, carousel_name="search_results")
else:
    # Example genres carousel
    genres = ["action", "history", "fantasy"]
    for genre in genres:
        st.subheader(f"🔥 {genre.capitalize()}")
        books = fetch_books(genre)
        create_carousel(books, books_per_page=3, carousel_name=genre)


# ---------------------------
# Multipage navigation
# ---------------------------
pages = {
    "Library": [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/reader.py", title="Reader")
    ],
    "Tools": [
        st.Page("pages/assistant.py", title="Library Assistant"),
        st.Page("pages/essay_writer.py", title="Essay Writer"),
        st.Page("pages/summarizer.py", title="Book Summarizer"),
        st.Page("pages/translator.py", title="Translator"),
        st.Page("pages/study_planner.py", title="Study Planner")
    ]
}

pg = st.navigation(pages, position="sidebar")
pg.run()
