# Dockerfile

# --- Base image: official Python slim image ---
# "slim" variant is much smaller than the full image (fewer pre-installed
# OS packages we don't need), which means faster builds and smaller
# final image size.
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# --- Install dependencies first (layer caching optimization) ---
# Copying only requirements.txt first means Docker only re-runs
# pip install when dependencies actually change, not on every
# code change.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Pre-download NLTK data at build time ---
# This avoids a runtime download delay/failure on the deployment
# server, which may have restricted network access.
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab')"

# --- Now copy the rest of the application code ---
COPY . .

# Streamlit's default port
EXPOSE 8501

# Container-level health check — lets orchestration platforms
# (and you) know if the app inside is actually responding, not
# just that the process is running.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the app. --server.address=0.0.0.0 is essential: without it,
# Streamlit binds only to localhost INSIDE the container, which
# makes it unreachable from outside — a very common Docker+Streamlit
# beginner mistake.
# CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]