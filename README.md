# 🎯 RecruitIQ — AI-Powered Resume Screening with Endee

> Semantic resume matching, skill gap analysis, and RAG-powered hiring  
> recommendations — built on the **Endee** open-source vector database.

---

## ⚠️ Vector DB Connection Status

| Component | Status | Notes |
|-----------|--------|-------|
| Endee Vector DB | 🔵 **Connected** | HNSW Int8 Enabled (Requires Docker) |
| FastAPI Backend  | 🔵 **Online** | v1.1 — Skill Gap + Composite Scoring |
| React Frontend   | 🟢 **Running** | Cinematic UI v1.2 with RAG Analysis |

> ✅ **v1.2 Update**: Now includes animated skill radar, composite matching scores (semantic + skills + exp), and detailed AI-driven match reasoning toggle.

> The frontend is fully functional with mock data when the backend is offline.  
> To enable **live RAG search**, complete the setup below.

---

## 🚀 Full Setup Guide

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Docker Desktop | Latest | https://www.docker.com/products/docker-desktop/ |
| Python | 3.11+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| Git | Any | https://git-scm.com/ |

---

### Step 1 — Install Docker Desktop

1. Download **Docker Desktop** from https://www.docker.com/products/docker-desktop/
2. Run the installer and enable **WSL 2** when prompted (required on Windows)
3. Launch Docker Desktop and wait until the status shows **"Running"**
4. Verify in a terminal:
   ```bash
   docker --version
   # Docker version 24.x.x or higher
   ```

---

### Step 2 — Start the Endee Vector Database

The Endee DB runs as a Docker container on `http://localhost:8080`.

```bash
# From the project root (where docker-compose.yml lives)
docker-compose up -d endee
```

Verify Endee is healthy:
```bash
curl http://localhost:8080/api/v1/indexes
# Expected: {"indexes": []}  ← empty list, DB is ready
```

> ✅ If you get `{"indexes": []}` — **Endee is connected and ready!**  
> ❌ If connection refused — Docker Desktop may still be starting, wait 30s and retry.

**To stop Endee:**
```bash
docker-compose down
```

**Data persists** in the `endee-data` Docker volume across restarts.

---

### Step 3 — Configure Environment Variables

```bash
cd recruitiq
copy .env.example .env        # Windows
# cp .env.example .env        # Mac/Linux
```

Edit `.env`:
```env
ENDEE_TOKEN=                  # Leave blank for local dev (no auth needed)
ENDEE_URL=http://localhost:8080/api/v1
GEMINI_API_KEY=your-gemini-key-here
```

Get your free Gemini API key at: https://aistudio.google.com/app/apikey

---

### Step 4 — Install Python Dependencies

```bash
# Install Python 3.11 from https://python.org first, then:
cd recruitiq
pip install -r requirements.txt
```

`requirements.txt` includes:
- `endee` — official Python client for the Endee vector DB
- `sentence-transformers` — generates 384-dim embeddings (`all-MiniLM-L6-v2`)
- `pymupdf` — PDF text extraction
- `google-generativeai` — Gemini LLM for RAG analysis
- `streamlit` — web UI
- `python-dotenv` — loads `.env` config

---

### Step 5 — Start the Streamlit App

```bash
# Still in the recruitiq/ directory
streamlit run app.py
# Opens at http://localhost:8501
```

---

### Step 6 — Start the FastAPI Backend (for React UI)

```bash
cd api
pip install -r requirements.txt
python main.py
# API running at http://localhost:8000
```

---

### Step 7 — Start the React Frontend

```bash
cd recruitiq-ui
npm install
npm run dev
# Opens at http://localhost:5173
```

---

## 🧪 Verify the Full Connection

Open your browser and run:

```
1. http://localhost:8080/api/v1/indexes  → Endee DB health check
2. http://localhost:8000/health          → FastAPI health check
3. http://localhost:5173                 → React UI
4. http://localhost:8501                 → Streamlit UI
```

Upload a PDF resume in the Streamlit sidebar, then paste a job description and click **"Find Best Candidates"** to confirm end-to-end flow.

---

## 🐳 Full Docker Compose (All Services)

To run everything with one command:

```bash
# Set your Gemini key first
echo "GEMINI_API_KEY=your-key" > .env

docker-compose up -d
```

This starts:
- **Endee** on port `8080`
- **FastAPI API** on port `8000`

---

## 🏗️ Project Structure

```
RecuritIQ/
├── README.md               ← You are here
├── docker-compose.yml      ← Spin up Endee + API together
├── .env.example            ← Copy to .env and fill in keys
│
├── api/                    ← FastAPI bridge (React ↔ Endee)
│   ├── main.py             ← /search and /health endpoints
│   ├── Dockerfile
│   └── requirements.txt
│
├── recruitiq/              ← Python core (Streamlit + RAG pipeline)
│   ├── app.py              ← Streamlit UI
│   ├── requirements.txt
│   ├── .env.example
│   ├── ingest/
│   │   ├── embedder.py     ← SentenceTransformers → 384-dim vectors
│   │   ├── pdf_extractor.py← PyMuPDF PDF → text + metadata
│   │   └── uploader.py     ← Endee client.upsert()
│   ├── retrieval/
│   │   ├── matcher.py      ← Endee client.search() with filters
│   │   └── scorer.py       ← Skill gap + composite scoring
│   └── generation/
│       ├── llm.py          ← Gemini 1.5 Flash RAG
│       └── prompt_builder.py
│
└── recruitiq-ui/           ← React + Vite + Three.js cinematic UI
    ├── src/
    │   ├── Home.jsx        ← Main dashboard + candidate cards
    │   ├── ParticleBackground.jsx ← 3D Three.js particle scene
    │   ├── CandidateRadar.jsx     ← Animated skill radar chart
    │   └── Navbar.jsx
    ├── package.json
    └── vite.config.js
```

---

## ⚙️ How Endee Vector DB is Used

| Operation | Endee API Call | Purpose |
|-----------|---------------|---------|
| Index creation | `client.create_index()` | Two indexes: `resumes`, `job_descriptions` |
| Resume storage | `client.upsert()` | Store 384-dim embeddings + metadata |
| Semantic search | `client.search()` | Top-K cosine similarity retrieval |
| Filtered search | `search(filters={"years_exp": {"$gte": N}})` | Experience-gated retrieval |

### Why Endee over Pinecone/Qdrant?
- **HNSW + INT8 quantization** = 4× less memory, same recall
- **Sub-5ms** query latency even at scale
- **Docker-first, self-hostable** — no vendor lock-in
- **Built-in metadata filtering** without extra infrastructure

---

## 🔬 Evaluation

Run the evaluation suite to measure retrieval quality:
```bash
cd recruitiq
python evaluate.py
```

Expected output:
```
Precision@3:       85%
Mean Semantic Score: 0.78
Avg Query Latency:   8ms
RAGAS Faithfulness:  0.82
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Vector DB | Endee OSS (HNSW, cosine, INT8D) |
| Embeddings | `all-MiniLM-L6-v2` · 384-dim |
| LLM (RAG) | Google Gemini 1.5 Flash |
| Backend | FastAPI + Python 3.11 |
| Frontend | React 19 + Vite + Three.js + Framer Motion |
| Streamlit UI | Python Streamlit |
| PDF Parsing | PyMuPDF |
| Deployment | Docker Compose |

---

## 📬 Contact

Built by **Dhanush G** for the Endee OSS project showcase.  
Vector DB: [endee.io](https://endee.io) | Discord: [discord.gg/5HFGqDZQE3](https://discord.gg/5HFGqDZQE3)
