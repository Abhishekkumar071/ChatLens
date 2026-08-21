# ui/activity.py
import streamlit as st
import pandas as pd
import plotly.express as px

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def render_activity_tab(df: pd.DataFrame):
    st.subheader("📈 Activity Over Time")

    # --- 1. Daily trend line ---
    daily_counts = df.groupby("date").size().reset_index(name="messages")
    fig_trend = px.line(
        daily_counts,
        x="date",
        y="messages",
        title="Messages per Day",
        markers=True,
    )
    fig_trend.update_layout(xaxis_title="Date", yaxis_title="Messages")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    # --- 2. Hourly distribution ---
    with col1:
        st.subheader("🕐 Activity by Hour")
        hourly_counts = df.groupby("hour").size().reset_index(name="messages")
        fig_hourly = px.bar(
            hourly_counts,
            x="hour",
            y="messages",
            title="Messages by Hour of Day",
        )
        fig_hourly.update_layout(xaxis_title="Hour (24h)", yaxis_title="Messages")
        st.plotly_chart(fig_hourly, use_container_width=True)

    # --- 3. Busiest day of week (simple bar, sets up the heatmap concept) ---
    with col2:
        st.subheader("📅 Activity by Day of Week")
        df_ordered = df.copy()
        df_ordered["day_name"] = pd.Categorical(
            df_ordered["day_name"], categories=DAY_ORDER, ordered=True
        )
        day_counts = df_ordered.groupby("day_name", observed=True).size().reset_index(name="messages")
        fig_day = px.bar(
            day_counts,
            x="day_name",
            y="messages",
            title="Messages by Day of Week",
        )
        fig_day.update_layout(xaxis_title="Day", yaxis_title="Messages")
        st.plotly_chart(fig_day, use_container_width=True)

    st.divider()

    # --- 4. Day x Hour heatmap ---
    st.subheader("🔥 Weekly Activity Heatmap")

    df_ordered = df.copy()
    df_ordered["day_name"] = pd.Categorical(
        df_ordered["day_name"], categories=DAY_ORDER, ordered=True
    )

    heatmap_data = (
        df_ordered.groupby(["day_name", "hour"], observed=True)
        .size()
        .reset_index(name="messages")
        .pivot(index="day_name", columns="hour", values="messages")
        .reindex(DAY_ORDER)  # enforce Monday->Sunday row order
        .fillna(0)
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Hour of Day", y="Day of Week", color="Messages"),
        aspect="auto",
        color_continuous_scale="Blues",
        title="When do you talk the most?",
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)