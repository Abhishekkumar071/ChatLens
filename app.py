# app.py
import streamlit as st
from parsers.telegram import parse_telegram_json
from parsers.whatsapp import parse_whatsapp_txt
from processing.enrich import messages_to_dataframe

st.set_page_config(
    page_title="ChatLens — Chat Analytics Dashboard",
    page_icon="💬",
    layout="wide",
)


def parse_uploaded_file(uploaded_file) -> "pd.DataFrame":
    """
    Detects platform from file extension and routes to the correct
    parser, then runs the result through the enrichment pipeline.
    """
    file_bytes = uploaded_file.read()

    if uploaded_file.name.endswith(".json"):
        messages = parse_telegram_json(file_bytes)
    elif uploaded_file.name.endswith(".txt"):
        messages = parse_whatsapp_txt(file_bytes)
    else:
        st.error("Unsupported file type. Please upload a Telegram (.json) or WhatsApp (.txt) export.")
        return None

    return messages_to_dataframe(messages)


def main():
    st.title("💬 ChatLens")
    st.caption("Chat Analytics Dashboard")

    with st.sidebar:
        st.header("Upload your chat")
        uploaded_file = st.file_uploader(
            "Telegram (.json) or WhatsApp (.txt) export",
            type=["json", "txt"],
        )

    # --- Stage 1: parse once, store in session_state ---
    # This block only runs when a NEW file is uploaded (we check the
    # filename against what's already stored, so re-running the script
    # from unrelated interactions doesn't re-parse the same file).
    if uploaded_file is not None:
        if st.session_state.get("uploaded_filename") != uploaded_file.name:
            with st.spinner("Parsing your chat..."):
                df = parse_uploaded_file(uploaded_file)
            if df is not None:
                st.session_state["chat_df"] = df
                st.session_state["uploaded_filename"] = uploaded_file.name

    # --- Stage 2: nothing uploaded yet ---
    if "chat_df" not in st.session_state:
        st.info("👈 Upload a chat export from the sidebar to get started.")
        return

    df = st.session_state["chat_df"]

    if df.empty:
        st.warning("No valid messages could be parsed from this file.")
        return

    # --- Stage 3: tab layout (placeholder content for now) ---
    tab_overview, tab_activity, tab_words, tab_search, tab_emoji = st.tabs(
        ["📊 Overview", "📈 Activity", "☁️ Words", "🔍 Search", "😂 Emoji"]
    )

    with tab_overview:
        st.write(f"Loaded **{len(df)}** messages. (Real stats coming in Step 10.)")
        st.dataframe(df.head())

    with tab_activity:
        st.write("Activity timeline coming in Step 11.")

    with tab_words:
        st.write("Word analysis coming in Step 12.")

    with tab_search:
        st.write("Word searcher coming in Step 13.")

    with tab_emoji:
        st.write("Emoji analytics coming in Step 14.")


if __name__ == "__main__":
    main()