# ui/overview.py
import streamlit as st
import pandas as pd


def render_overview_tab(df: pd.DataFrame):
    st.subheader("📊 Chat Overview")

    # --- Top-level headline stats ---
    total_messages = len(df)
    total_words = int(df["word_count"].sum())
    total_media = int(df["is_media"].sum())
    active_days = df["date"].nunique()
    participants = df["sender"].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Messages", f"{total_messages:,}")
    col2.metric("Total Words", f"{total_words:,}")
    col3.metric("Media Shared", f"{total_media:,}")
    col4.metric("Active Days", f"{active_days:,}")
    col5.metric("Participants", participants)

    st.divider()

    # --- Per-sender breakdown ---
    st.subheader("👥 Per-Sender Breakdown")

    sender_stats = (
        df.groupby("sender")
        .agg(
            messages=("text", "count"),
            words=("word_count", "sum"),
            media=("is_media", "sum"),
        )
        .sort_values("messages", ascending=False)
    )

    sender_stats["avg_words_per_message"] = (
        sender_stats["words"] / sender_stats["messages"]
    ).round(1)

    sender_stats["share_of_messages_%"] = (
        (sender_stats["messages"] / total_messages) * 100
    ).round(1)

    st.dataframe(
        sender_stats,
        use_container_width=True,
        column_config={
            "messages": st.column_config.NumberColumn(format="%d"),
            "words": st.column_config.NumberColumn(format="%d"),
            "media": st.column_config.NumberColumn(format="%d"),
            "share_of_messages_%": st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100
            ),
        },
    )

    # --- Date range context ---
    st.caption(
        f"📅 Chat spans from **{df['date'].min()}** to **{df['date'].max()}**"
    )
    