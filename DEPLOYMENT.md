# 🚀 PaperPulse AI — Deployment Guide

> Complete reference for deploying PaperPulse AI to **Streamlit Community Cloud**, **Docker**, **Local Environments**, and **Cloud VMs / VPS**.

---

## 📑 Table of Contents
1. [Streamlit Community Cloud (Recommended)](#1-streamlit-community-cloud-recommended)
2. [Local Environment Deployment](#2-local-environment-deployment)
3. [Docker Container Deployment](#3-docker-container-deployment)
4. [Cloud VM / VPS Deployment (Systemd + Nginx)](#4-cloud-vm--vps-deployment-systemd--nginx)
5. [Environment Variables & Secrets Reference](#5-environment-variables--secrets-reference)
6. [Health Check & Verification](#6-health-check--verification)

---

## 1. Streamlit Community Cloud (Recommended)

Streamlit Community Cloud provides **100% free hosting** with automatic CI/CD directly linked to your GitHub repository.

### Step 1: Sign in to Streamlit Cloud
1. Navigate to **[share.streamlit.io](https://share.streamlit.io/)**.
2. Sign in with your GitHub account.

### Step 2: Create New Deployment
1. Click **"New app"** (or **"Create app"**).
2. Select **"I already have an app"** and fill in the deployment details:

| Parameter | Value |
| :--- | :--- |
| **Repository** | `callme-siva/PaperPulse_AI` *(or your fork)* |
| **Branch** | `main` |
| **Main file path** | `app.py` |
| **App URL** | `paperpulse-studio.streamlit.app` |
| **Live Instance** | **[https://paperpulse-studio.streamlit.app](https://paperpulse-studio.streamlit.app)** |

### Step 3: Advanced Settings (Python Version & Secrets)
Click **"Advanced settings"** before deploying:
* **Python version**: Choose **`3.11`** or **`3.10`**.
* **Secrets (TOML format)**: Paste any optional API keys:

```toml
# Streamlit Cloud Secrets (TOML format)
GEMINI_API_KEY = "AIzaSy..."
OPENAI_API_KEY = "sk-proj-..."
GROQ_API_KEY = "gsk_..."

# Active Model Selection
LLM_PROVIDER = "gemini"
LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

> 💡 **Note**: PaperPulse AI runs **100% offline out-of-the-box** even with 0 API keys using local sentence embeddings and deterministic synthesis.

### Step 4: Deploy!
* Click **"Deploy!"**.
* The build process will automatically install [`requirements.txt`](file:///Users/siva/AI-codebase/PaperPulse_AI/requirements.txt) and launch the application in ~60-90 seconds.
* Every subsequent `git push origin main` triggers an instant, zero-downtime rebuild.

---

## 2. Local Environment Deployment

### Prerequisites
* Python 3.10, 3.11, or 3.12+
* Git

### Step-by-Step Setup
```bash
# 1. Clone the repository
git clone https://github.com/callme-siva/PaperPulse_AI.git
cd PaperPulse_AI

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. (Optional) Configure environment variables
cp .env.example .env
# Edit .env to add your GEMINI_API_KEY, OPENAI_API_KEY, or GROQ_API_KEY

# 5. Run the Streamlit application
streamlit run app.py
```

The app will be accessible at:
* Local URL: `http://localhost:8501`
* Network URL: `http://<your-lan-ip>:8501`

---

## 3. Docker Container Deployment

### Create `Dockerfile`
Create a `Dockerfile` in the root directory:

```dockerfile
FROM python:3.11-slim

# Set working directory & environment variables
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build & Run Container
```bash
# Build Docker image
docker build -t paperpulse-ai:latest .

# Run container with optional environment variables
docker run -d \
  -p 8501:8501 \
  -e GEMINI_API_KEY="your_api_key_here" \
  -e LLM_PROVIDER="gemini" \
  --name paperpulse-container \
  paperpulse-ai:latest
```

---

## 4. Cloud VM / VPS Deployment (Systemd + Nginx)

For persistent hosting on AWS EC2, GCP Compute Engine, or DigitalOcean Droplets.

### A. Create Systemd Service Unit
Create `/etc/systemd/system/paperpulse.service`:

```ini
[Unit]
Description=PaperPulse AI Streamlit Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/PaperPulse_AI
Environment="PATH=/home/ubuntu/PaperPulse_AI/venv/bin"
ExecStart=/home/ubuntu/PaperPulse_AI/venv/bin/streamlit run app.py --server.port=8501 --server.headless=true --server.address=127.0.0.1
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable paperpulse
sudo systemctl start paperpulse
```

### B. Configure Nginx Reverse Proxy with WebSocket Support
Create `/etc/nginx/sites-available/paperpulse`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/paperpulse /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 5. Environment Variables & Secrets Reference

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | Secret | `""` | Google Gemini API Key (e.g. `AIzaSy...`) |
| `OPENAI_API_KEY` | Secret | `""` | OpenAI API Key (e.g. `sk-proj-...`) |
| `GROQ_API_KEY` | Secret | `""` | Groq Cloud API Key (e.g. `gsk_...`) |
| `LLM_PROVIDER` | String | `gemini` | Active provider (`gemini`, `openai`, `groq`) |
| `LLM_MODEL` | String | `gemini-2.5-flash` | Active model identifier |
| `EMBEDDING_MODEL` | String | `all-MiniLM-L6-v2` | SentenceTransformer model |
| `SECTION_CHUNK_SIZE` | Integer | `500` | Section chunk character length |
| `SECTION_CHUNK_OVERLAP` | Integer | `75` | Section chunk overlap characters |
| `TOP_K_PAPERS` | Integer | `5` | Top-K papers retrieved per query |
| `SIMILARITY_THRESHOLD` | Float | `0.35` | Minimum cosine relevance threshold $\tau$ |

---

## 6. Health Check & Verification

Run health checks against the running server:
```bash
# Verify Streamlit internal health status
curl -s http://localhost:8501/_stcore/health
# Expected Output: ok

# Run full automated test suite (39 tests)
pytest -v
```
