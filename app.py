# app.py
import streamlit as st
from parsers.telegram import parse_telegram_json
from parsers.whatsapp import parse_whatsapp_txt
from processing.enrich import messages_to_dataframe
from ui.overview import render_overview_tab
from ui.activity import render_activity_tab
from ui.words import render_words_tab
from ui.search import render_search_tab
from ui.emoji_tab import render_emoji_tab

st.set_page_config(
    page_title="ChatLens — Chat Analytics Dashboard",
    page_icon="💬",
    layout="wide",
)


# def parse_uploaded_file(uploaded_file) -> "pd.DataFrame":
#     """
#     Detects platform from file extension and routes to the correct
#     parser, then runs the result through the enrichment pipeline.
#     """
#     file_bytes = uploaded_file.read()

#     if uploaded_file.name.endswith(".json"):
#         messages = parse_telegram_json(file_bytes)
#     elif uploaded_file.name.endswith(".txt"):
#         messages = parse_whatsapp_txt(file_bytes)
#     else:
#         st.error("Unsupported file type. Please upload a Telegram (.json) or WhatsApp (.txt) export.")
#         return None

#     return messages_to_dataframe(messages)

# # app.py — parse_uploaded_file() ko replace karo is version se

import json

MAX_REASONABLE_SIZE_MB = 200


def parse_uploaded_file(uploaded_file) -> "pd.DataFrame":
    """
    Detects platform from file extension and routes to the correct
    parser. Wrapped in error handling so any unexpected failure
    (corrupted file, wrong format, encoding issue) shows the user a
    clean message instead of crashing the app with a raw traceback.
    """
    file_bytes = uploaded_file.read()

    # --- Guard: empty file ---
    if len(file_bytes) == 0:
        st.error("This file appears to be empty. Please upload a valid chat export.")
        return None

    # --- Guard: unreasonably large (defense-in-depth beyond config.toml limit) ---
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_REASONABLE_SIZE_MB:
        st.error(f"File is too large ({size_mb:.1f}MB). Please upload a file under {MAX_REASONABLE_SIZE_MB}MB.")
        return None

    try:
        if uploaded_file.name.endswith(".json"):
            messages = parse_telegram_json(file_bytes)
        elif uploaded_file.name.endswith(".txt"):
            messages = parse_whatsapp_txt(file_bytes)
        else:
            st.error("Unsupported file type. Please upload a Telegram (.json) or WhatsApp (.txt) export.")
            return None
    except json.JSONDecodeError:
        st.error("This doesn't look like a valid Telegram JSON export — the file couldn't be parsed as JSON.")
        return None
    except UnicodeDecodeError:
        st.error("This file's encoding couldn't be read. Please make sure it's a plain text export.")
        return None
    except Exception:
        # Last-resort safety net: never let an unexpected error crash
        # the app with a raw traceback in front of the user.
        traceback.print_exc()   # TEMPORARY — terminal mein pura error dikhayega
        st.error("Something went wrong while processing this file. Please make sure it's a valid, unmodified chat export.")
        return None

    df = messages_to_dataframe(messages)

    if df.empty:
        st.warning("No valid messages could be found in this file. It may be empty, corrupted, or in an unsupported format.")
        return None

    return df


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

    # with tab_overview:
    #     st.write(f"Loaded **{len(df)}** messages. (Real stats coming in Step 10.)")
    #     st.dataframe(df.head())

    with tab_overview:
        render_overview_tab(df)

    with tab_activity:
        render_activity_tab(df)

    with tab_words:
        render_words_tab(df)

    with tab_search:
        render_search_tab(df)
    
    with tab_emoji:
        render_emoji_tab(df)


if __name__ == "__main__":
    main()