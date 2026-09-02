# ui/words.py
import streamlit as st
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def _ensure_nltk_data():
    """
    NLTK's stopwords/tokenizer data isn't bundled in the pip package —
    it must be downloaded once. This checks if it's already present,
    and downloads only if missing, so the app self-heals on any fresh
    environment (a new machine, or the deployment server in Step 19)
    without manual setup.
    """
    resources = {
        "corpora/stopwords": "stopwords",
        "tokenizers/punkt_tab": "punkt_tab",
    }
    for path, package in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)

@st.cache_data(show_spinner=False)
def _get_word_frequencies(df: pd.DataFrame, min_word_length: int = 2) -> Counter:
    """
    Tokenizes all non-media message text, lowercases it, strips
    stopwords and punctuation-only tokens, and returns a Counter
    of word -> frequency.
    """
    _ensure_nltk_data()
    stop_words = set(stopwords.words("english"))

    all_text = " ".join(df.loc[~df["is_media"], "text"].astype(str))
    tokens = word_tokenize(all_text.lower())

    filtered = [
        t for t in tokens
        if t.isalpha()  # drops punctuation, numbers, emoji tokens
        and t not in stop_words
        and len(t) >= min_word_length
    ]

    return Counter(filtered)


def render_words_tab(df: pd.DataFrame):
    st.subheader("☁️ Word Analysis")

    # word_freq = _get_word_frequencies(df)
    word_freq = _get_word_frequencies(df[["text", "is_media"]])

    if not word_freq:
        st.info("Not enough text data to analyze (mostly media messages?).")
        return

    col1, col2 = st.columns([1, 1])

    # --- Word Cloud (Matplotlib, static image) ---
    with col1:
        st.subheader("Word Cloud")
        wc = WordCloud(
            width=800,
            height=500,
            background_color="#1c1e21",  # matches our dark theme from Step 3
            colormap="Blues",
        ).generate_from_frequencies(word_freq)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    # --- Top Words Bar Chart (Plotly, exact numbers) ---
    with col2:
        st.subheader("Top 15 Words")
        top_words = pd.DataFrame(
            word_freq.most_common(15), columns=["word", "count"]
        )
        fig_bar = px.bar(
            top_words.sort_values("count"),
            x="count",
            y="word",
            orientation="h",
            title="Most Frequent Words",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        