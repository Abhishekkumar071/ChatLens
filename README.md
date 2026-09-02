<div align="center">

# 💬 ChatLens — Chat Analytics Dashboard

<p><strong>Turn your conversations into patterns, peaks, and personality.</strong></p>

<p>
     <a href="https://github.com/Abhishekkumar071/ChatLens"><img src="https://img.shields.io/badge/status-active-2ea44f?style=for-the-badge" alt="Project status: active"></a>
     <a href="https://chatlens-8n5w26abhi.streamlit.app/"><img src="https://img.shields.io/badge/demo-live-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live demo"></a>
     <a href="https://github.com/Abhishekkumar071/ChatLens/actions"><img src="https://img.shields.io/badge/CI-passing-2ea44f?style=for-the-badge&logo=githubactions&logoColor=white" alt="CI passing"></a>
     <a href="https://github.com/Abhishekkumar071/ChatLens/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-111827?style=for-the-badge" alt="MIT License"></a>
</p>

**[🌐 Try the live demo →](https://chatlens-8n5w26abhi.streamlit.app/)**

</div>

**ChatLens** turns your exported Telegram or WhatsApp chat history into an interactive analytics dashboard — message trends, activity heatmaps, word clouds, a word search engine, and emoji leaderboards. Everything runs **locally**: your chat data is parsed and analyzed on your own machine and never sent to any external server.

<p align="center">
     <a href="#-features">Features</a> ·
     <a href="#-preview">Preview</a> ·
     <a href="#-how-to-export-your-chats">Export chats</a> ·
     <a href="#-installation--setup">Run locally</a> ·
     <a href="#-running-tests">Tests</a> ·
     <a href="#-deployment--engineering">Engineering</a>
</p>

---

## 🖼️ Preview

<p align="center">
     <a href="outPut_Image/overView_HomePage.png">
          <img src="outPut_Image/overView_HomePage.png" alt="ChatLens overview dashboard" width="920">
     </a>
</p>

<details>
<summary><strong>Explore every analytics view</strong> · click to expand</summary>

<table>
     <tr>
          <td align="center" width="50%"><a href="outPut_Image/activityOvertimeGraph.png"><img src="outPut_Image/activityOvertimeGraph.png" alt="Activity over time" width="100%"></a><br><sub>Activity over time</sub></td>
          <td align="center" width="50%"><a href="outPut_Image/activityByday%26hour.png"><img src="outPut_Image/activityByday%26hour.png" alt="Activity by day and hour" width="100%"></a><br><sub>Activity by day and hour</sub></td>
     </tr>
     <tr>
          <td align="center"><a href="outPut_Image/weekendActivityHeatmap.png"><img src="outPut_Image/weekendActivityHeatmap.png" alt="Weekly activity heatmap" width="100%"></a><br><sub>Weekly activity heatmap</sub></td>
          <td align="center"><a href="outPut_Image/wordAnanlysis.png"><img src="outPut_Image/wordAnanlysis.png" alt="Word analysis" width="100%"></a><br><sub>Word analysis</sub></td>
     </tr>
     <tr>
          <td align="center"><a href="outPut_Image/wordSercher.png"><img src="outPut_Image/wordSercher.png" alt="Word searcher" width="100%"></a><br><sub>Word searcher</sub></td>
          <td align="center"><a href="outPut_Image/emojisAnalysis.png"><img src="outPut_Image/emojisAnalysis.png" alt="Emoji analytics" width="100%"></a><br><sub>Emoji analytics</sub></td>
     </tr>
</table>
</details>

---

## ✨ Features

### 📊 Overview
Headline stats at a glance — total messages, words, media shared, active days, and participants — plus a per-sender breakdown showing who talks the most, average words per message, and share of conversation.

### 📈 Activity Timeline
- Daily message-volume trend line
- Hour-of-day activity distribution
- A day-of-week × hour **heatmap** — see exactly when you talk the most (late-night weekdays? Sunday mornings?)

### ☁️ Word Analysis
NLP-powered word frequency analysis using NLTK stopword filtering — cutting out noise words to surface the words that actually define your conversations. Includes a visual word cloud and a top-15 frequency bar chart.

### 🔍 Word Searcher
Search any word and instantly see who said it most, and a timeline of exactly when it was said across your chat history.

### 😂 Emoji Analytics
Extracts and counts every emoji used, showing overall top emojis, a per-person emoji leaderboard, and each participant's "signature emoji."

---

## 🏗️ Architecture

ChatLens is built as a modular pipeline rather than a single script:

```
  Raw Export (.json / .txt)
        │
        ▼
     parsers/          →  Platform-specific parsing (Telegram JSON / WhatsApp TXT)
        │                Outputs validated Message objects (Pydantic)
        ▼
   processing/        →  Feature engineering: word counts, timestamps,
        |                 emoji extraction — one shared enriched DataFrame
        ▼
       ui/                →  Five independent tab modules, each consuming
        |                     the same DataFrame (Overview, Activity, Words,Search, Emoji)
        ▼
      app.py             →  Thin orchestration layer — upload handling,
                          session state, tab routing, error handling, logging
```

**Why this matters:** parsing logic, data validation, and UI rendering are fully decoupled. Adding support for a new chat platform means writing one new parser — nothing else in the app changes.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| UI / Framework | [Streamlit](https://streamlit.io/) |
| Data Validation | [Pydantic](https://docs.pydantic.dev/) (frozen, hashable models) |
| Data Processing | [Pandas](https://pandas.pydata.org/) |
| Visualization | [Plotly](https://plotly.com/python/), [WordCloud](https://github.com/amueller/word_cloud), Matplotlib |
| NLP | [NLTK](https://www.nltk.org/) |
| Emoji Parsing | [emoji](https://pypi.org/project/emoji/) |
| Testing | [pytest](https://pytest.org/) |
| Containerization | [Docker](https://www.docker.com/) |
| CI/CD | [GitHub Actions](https://github.com/features/actions) (lint + test on every push) |
| Deployment | [Streamlit Community Cloud](https://streamlit.io/cloud) |

---

## 📥 How to Export Your Chats

### 📱 Telegram (Desktop)
1. Open Telegram Desktop → go to the chat you want to analyze.
2. Click the three dots (top right) → **Export chat history**.
3. Uncheck all media types (keeps the file small).
4. Under "Format", select **Machine-readable JSON**.
5. Export and upload the resulting `result.json` file to the app.

### 🟢 WhatsApp (Mobile)
1. Open WhatsApp → go to the chat → tap the contact/group name.
2. Scroll down → tap **Export Chat**.
3. Choose **Without Media**.
4. Save the `.txt` file and upload it to the app.

---

## 🚀 Installation & Setup

### Option A — Run locally
```bash
# 1. Clone the repository
git clone https://github.com/Abhishekkumar071/ChatLens.git
cd ChatLens

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```
The dashboard opens automatically at `http://localhost:8501`.

### Option B — Run with Docker
```bash
docker build -t chatlens:latest .
docker run -p 8501:8501 chatlens:latest
```

### Option C — Just use the live demo
No install needed → **[chatlens-8n5w26abhi.streamlit.app](https://chatlens-8n5w26abhi.streamlit.app/)**

---

## 🧪 Running Tests

```bash
pytest -v
```

Parsers and the preprocessing pipeline are covered with a `pytest` suite using synthetic fixture files (no real chat data required to run tests). Every push and pull request also runs this suite automatically via GitHub Actions, along with `ruff` linting.

---

## 📂 Project Structure

```
ChatLens/
├── app.py                    # Entry point — upload handling, tab routing, error handling, logging
├── models.py                  # Message data model (Pydantic, immutable/hashable)
├── parsers/
│   ├── telegram.py            # Telegram JSON parser
│   └── whatsapp.py            # WhatsApp TXT parser (multi-line, regional dates)
├── processing/
│   └── enrich.py               # Feature engineering pipeline (cached)
├── ui/
│   ├── overview.py
│   ├── activity.py
│   ├── words.py
│   ├── search.py
│   └── emoji_tab.py
├── tests/                      # pytest suite + fixtures
├── .github/workflows/
│   └── ci.yml                   # Automated lint + test on every push
├── .streamlit/
│   └── config.toml               # Dark theme configuration
├── Dockerfile
├── requirements.txt
└── pytest.ini
```

---

## 🔒 Deployment & Engineering

ChatLens isn't just a script — it's built and shipped like a real product:

- ✅ **Validated data pipeline** — Pydantic models catch malformed data at the boundary, not deep inside a chart function
- ✅ **Tested** — `pytest` suite covering both parsers and the preprocessing pipeline
- ✅ **Cached** — `st.cache_data` avoids redundant recomputation, stays responsive on 50k+ message chats
- ✅ **Hardened** — graceful handling of malformed/empty/oversized uploads, no raw tracebacks shown to users, server-side error logging
- ✅ **Containerized** — a working `Dockerfile` for reproducible, portable deployment
- ✅ **Continuously integrated** — every push runs linting (`ruff`) and the full test suite via GitHub Actions
- ✅ **Live deployed** — [chatlens-8n5w26abhi.streamlit.app](https://chatlens-8n5w26abhi.streamlit.app/)

---

## 🔮 Future Scope

The app is fully functional, tested, and live. Ideas being considered next:

- [ ] **Multi-platform support** — Discord and Instagram DM exports
- [ ] **AI-powered chat summarization** — optional LLM-based "what happened this week" summary
- [ ] **Exportable reports** — download a PDF/image summary of the dashboard
- [ ] **Group chat mode improvements** — better handling for chats with 10+ participants
- [ ] **Custom date-range filtering** — analyze a specific time window instead of the whole history

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions and guidelines.

---

## 💻 Privacy

ChatLens runs entirely on your local machine (or your own deployed instance). No chat data is uploaded to any third-party server, logged externally, or stored beyond your current session.

---

## 📝 License

MIT License — free to use, modify, and build on.

---

<p align="center">Built with ❤️ — a chat analytics dashboard, from scratch to production.<br>⭐ Star this repo if you find it useful!</p>