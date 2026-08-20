# 🔵 ChatLens — Chat Analytics Dashboard

ChatLens is a **chat analytics dashboard** built with Python and Streamlit.

It allows users to upload chat exports from platforms like **WhatsApp and Telegram** and explore useful insights such as message activity, word usage, emojis, and sender statistics.

> 🚧 **Project Status:** In Development

---

## ✨ Features

Currently, ChatLens is being developed with the following features in mind:

- 📊 Chat activity analytics
- 👥 Sender-wise message statistics
- 🕐 Activity by date, day, and hour
- 🔤 Word frequency analysis
- 🔎 Search messages and words
- 😀 Emoji analytics
- 📱 WhatsApp chat export support
- ✈️ Telegram JSON export support
- 📈 Interactive charts using Plotly

More features will be added as development continues.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — Web dashboard
- **Pandas** — Data processing
- **Pydantic** — Data validation
- **Plotly** — Interactive visualizations
- **NLTK** — Text processing
- **WordCloud** — Word visualization
- **Pytest** — Testing

---

## 📁 Project Structure

The project is being developed with a modular structure:

```text
ChatLens/
│
├── app.py
├── models.py
├── requirements.txt
│
├── parsers/
│   ├── telegram.py
│   └── whatsapp.py
│
├── processing/
│   └── enrich.py
│
├── tests/
│
├── .gitignore
└── README.md