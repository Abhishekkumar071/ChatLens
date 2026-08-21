# ui/emoji_tab.py
import streamlit as st
import pandas as pd
import plotly.express as px


def render_emoji_tab(df: pd.DataFrame):
    st.subheader("😂 Emoji Analytics")

    # Explode: one row per individual emoji, not per message.
    # Rows with an empty emoji list are dropped automatically by explode
    # producing NaN, which we filter out next.
    exploded = df[["sender", "emojis"]].explode("emojis").dropna(subset=["emojis"])

    if exploded.empty:
        st.info("No emojis found in this chat.")
        return

    total_emojis = len(exploded)
    unique_emojis = exploded["emojis"].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Emoji Sent", f"{total_emojis:,}")
    col2.metric("Unique Emojis Used", unique_emojis)

    st.divider()

    col_left, col_right = st.columns(2)

    # --- Overall top emoji ---
    with col_left:
        st.subheader("Top Emojis (Overall)")
        top_overall = (
            exploded["emojis"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_overall.columns = ["emoji", "count"]
        fig_overall = px.bar(
            top_overall.sort_values("count"),
            x="count",
            y="emoji",
            orientation="h",
            title="Most Used Emojis",
        )
        st.plotly_chart(fig_overall, use_container_width=True)

    # --- Who uses emoji the most ---
    with col_right:
        st.subheader("Emoji Leaderboard")
        sender_emoji_counts = (
            exploded.groupby("sender")
            .size()
            .reset_index(name="emoji_count")
            .sort_values("emoji_count", ascending=False)
        )
        fig_leaderboard = px.bar(
            sender_emoji_counts,
            x="sender",
            y="emoji_count",
            title="Total Emoji Sent per Person",
        )
        st.plotly_chart(fig_leaderboard, use_container_width=True)

    st.divider()

    # --- Per-sender top emoji (the "personality" view) ---
    st.subheader("Each Person's Signature Emoji")
    top_per_sender = (
        exploded.groupby(["sender", "emojis"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .groupby("sender")
        .first()  # top emoji per sender, since already sorted by count desc
        .reset_index()
        .rename(columns={"emojis": "top_emoji"})
    )
    st.dataframe(
        top_per_sender[["sender", "top_emoji", "count"]],
        use_container_width=True,
        hide_index=True,
    )