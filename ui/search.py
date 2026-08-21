# ui/search.py
import streamlit as st
import pandas as pd
import re
import plotly.express as px


def render_search_tab(df: pd.DataFrame):
    st.subheader("🔍 Word Searcher")

    search_term = st.text_input(
        "Search for a word",
        placeholder="e.g. movie, birthday, project...",
    ).strip()

    # --- Guard clause: nothing typed yet ---
    if not search_term:
        st.info("Type a word above to see who said it, and when.")
        return

    # Whole-word, case-insensitive match using a regex word boundary.
    # re.escape() prevents special regex characters in user input
    # (like "?" or "(") from being interpreted as regex syntax.
    pattern = rf"\b{re.escape(search_term.lower())}\b"

    mask = (
        df["text"]
        .astype(str)
        .str.lower()
        .str.contains(pattern, regex=True, na=False)
    )
    matches = df[mask]

    # --- Guard clause: no matches found ---
    if matches.empty:
        st.warning(f"No messages found containing **\"{search_term}\"**.")
        return

    st.success(f"Found **{len(matches)}** messages containing **\"{search_term}\"**")

    col1, col2 = st.columns([1, 1])

    # --- Per-sender breakdown ---
    with col1:
        st.subheader("Who said it most")
        sender_counts = (
            matches.groupby("sender")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
        )
        fig_bar = px.bar(
            sender_counts,
            x="sender",
            y="count",
            title=f'Mentions of "{search_term}" by sender',
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Timeline of mentions ---
    with col2:
        st.subheader("When it was said")
        daily_counts = (
            matches.groupby("date")
            .size()
            .reset_index(name="count")
        )
        fig_line = px.line(
            daily_counts,
            x="date",
            y="count",
            markers=True,
            title=f'"{search_term}" mentions over time',
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # --- Raw matching messages, for context ---
    with st.expander(f"View all {len(matches)} matching messages"):
        st.dataframe(
            matches[["timestamp", "sender", "text"]].sort_values("timestamp", ascending=False),
            use_container_width=True,
        )