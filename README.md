# **RECRUITIQ — AI-POWERED RESUME SCREENING WITH ENDEE VECTOR DATABASE**

**A Full-Stack Semantic Hiring Intelligence Platform**

---

## 📌 Overview

**RecruitIQ** is a production-ready, full-stack **AI-powered resume screening and candidate matching system** built for elite technical recruitment. It is powered by the **Endee open-source vector database** for sub-millisecond semantic search, **OpenAI-compatible embedding APIs** for dense vector generation, and a **cinematic React frontend** for an exceptional user experience.

The system enables recruiters to:

- **Upload PDF resumes** — automatically extracted, embedded, and indexed into Endee
- **Search semantically** — paste a job description and retrieve the most relevant candidates using HNSW cosine similarity
- **Score comprehensively** — composite score = 50% semantic + 35% skill match + 15% experience
- **Generate AI analysis** — LLM-powered hiring recommendation, concern flags, and interview questions per candidate

The platform is designed to be:

- 🚀 **Fast** — Sub-5ms vector queries via Endee's HNSW + INT8D quantization
- 🧠 **Intelligent** — RAG pipeline combining semantic search with LLM screening
- 🎨 **Beautiful** — Cinematic glassmorphism UI with Three.js particle background
- 🐳 **Self-hostable** — Fully Docker-based, no vendor lock-in

---

## 🖥️ Tech Stack

### Frontend
- **React 19** + Vite
- **Framer Motion** — cinematic page transitions and micro-animations
- **Three.js** — 3D interactive particle background
- **Lucide React** — icon system
- **Vanilla CSS** — glassmorphism design system

### Backend
- **FastAPI** (Python 3.11)
- **Endee Python SDK** (`endee>=0.1.25`) — official vector DB client
- **OpenAI-compatible API** — Together AI / Gemini / OpenAI for embeddings + LLM
- **PyMuPDF** — PDF text extraction
- **Uvicorn** — ASGI server

### Vector Database
- **Endee OSS** — HNSW graph index, cosine similarity, INT8D quantization
- **Self-hosted via Docker** on `http://localhost:8080`
- Index names: `recruitiq_resumes`, `recruitiq_jds`
- Embedding dimension: **1024-dim** (multilingual-e5-large-instruct)

### Deployment
- **Endee**: Docker container (local or cloud)
- **FastAPI Backend**: Docker or direct Python
- **React Frontend**: Vite dev server (`http://localhost:5173`)
- **Streamlit UI** (alt): `http://localhost:8501`

---

## 📂 Project Structure

```
RecuritIQ_Endee_Project/
│
├── backend/                        ← FastAPI backend (v2 — Endee SDK)
│   ├── main.py                     ← /health /upload /search endpoints
│   ├── config.py                   ← All env var loading
│   ├── endee_client.py             ← Endee SDK: create_index, upsert, search
│   ├── embedder.py                 ← OpenAI-compat embeddings
│   ├── ingest.py                   ← PDF → text → embed → upsert pipeline
│   ├── agent.py                    ← RAG pipeline: score + LLM screening
│   ├── requirements.txt
│   └── Dockerfile
│
├── recruitiq-ui/                   ← React cinematic frontend
│   ├── src/
│   │   ├── Home.jsx                ← Main dashboard, search, candidate cards
│   │   ├── ParticleBackground.jsx  ← Three.js 3D particle scene
│   │   ├── CandidateRadar.jsx      ← Animated skill radar chart
│   │   ├── Navbar.jsx
│   │   ├── App.jsx
│   │   ├── App.css                 ← Glassmorphism design system
│   │   └── index.css               ← CSS tokens
│   ├── package.json
│   └── vite.config.js
│
├── endee/recruitiq/                ← Streamlit UI (alternate interface)
│   ├── app.py                      ← Streamlit resume screening app
│   ├── ingest/                     ← PDF extractor, embedder, uploader
│   ├── retrieval/                  ← matcher.py, scorer.py
│   ├── generation/                 ← llm.py, prompt_builder.py
│   └── requirements.txt
│
├── api/                            ← Legacy FastAPI bridge (v1)
│   ├── main.py
│   └── Dockerfile
│
├── docker-compose.yml              ← Endee + FastAPI together
├── .env.example                    ← Copy to .env and fill keys
└── README.md
```

---

## ✨ Key Features

### 🔍 Semantic Search Engine
- Job description embedded into 1024-dim vector
- Endee HNSW index performs cosine similarity search
- Top-K candidates retrieved in < 5ms
- Optional metadata filter: `years_exp >= N`

### 📊 Composite Scoring System
- **50% Semantic Score** — vector cosine similarity (Endee)
- **35% Skill Match** — keyword overlap with job requirements
- **15% Experience Score** — years of experience normalized

### 🤖 AI Screening (RAG)
- LLM generates per-candidate analysis:
  - `recommendation`: STRONG FIT / GOOD FIT / PARTIAL FIT / NOT FIT
  - `hire_reason`: 2–3 sentence justification
  - `concern`: Key risk or gap
  - `interview_questions`: 3 tailored questions

### 📤 PDF Resume Ingestion
- Upload single or bulk PDF resumes
- Auto-extracts: name, email, skills, years of experience
- Embeds first 2000 chars using multilingual-e5 model
- Upserts into Endee with flat metadata schema

### 🎨 Cinematic UI
- Three.js 3D animated particle background
- Glassmorphism candidate cards
- Color-coded recommendation badges (STRONG / GOOD / PARTIAL / NOT FIT)
- Expandable AI analysis panel per candidate
- Real-time upload toast notifications
- Endee DB live status indicator

### ⚡ Endee Vector DB (INT8D + HNSW)
- **4× less memory** than float32 vectors with same recall
- **Sub-5ms** query latency even at scale
- **Built-in metadata filtering** — no extra infrastructure
- **Docker-first** — no vendor lock-in, fully self-hostable

---

## 🚀 Full Setup Guide

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Docker Desktop | Latest | https://www.docker.com/products/docker-desktop/ |
| WSL 2 (Windows) | Required for Docker | `wsl --install` in admin PowerShell |
| Python | 3.11+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| Git | Any | https://git-scm.com/ |

---

### Step 1 — Install WSL2 (Windows only)

Open PowerShell as **Administrator** and run:

```powershell
wsl --install
# Restart your PC after this completes
```

After restart, Docker Desktop will be able to use the Linux engine.

---

### Step 2 — Start Endee Vector DB

```bash
# Pull and run Endee OSS server
docker run -d \
  -p 8080:8080 \
  -v endee-data:/data \
  --name endee-server \
  endeeio/endee-server:latest

# Verify Endee is live
curl http://localhost:8080/api/v1/indexes
# Expected: {"indexes": []}   ← DB is ready!
```

> ✅ `{"indexes": []}` — **Endee is connected and ready!**
> ❌ Connection refused — wait 30s for container to fully start, then retry.

---

### Step 3 — Configure Environment Variables

```bash
# From project root
cp .env.example .env
```

Edit `.env`:

```env
# Option A: Together AI (free tier — recommended)
OPENAI_API_KEY=your-together-ai-key-here
OPENAI_BASE_URL=https://api.together.xyz/v1
EMBED_MODEL=intfloat/multilingual-e5-large-instruct
EMBED_DIM=1024
LLM_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo

# Option B: Gemini via OpenAI-compat
# OPENAI_API_KEY=your-gemini-key
# OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
# EMBED_MODEL=text-embedding-004
# EMBED_DIM=768
# LLM_MODEL=gemini-1.5-flash

# Endee Vector DB
ENDEE_URL=http://localhost:8080/api/v1
ENDEE_TOKEN=
INDEX_NAME=recruitiq_resumes
JD_INDEX_NAME=recruitiq_jds
```

Get a **free** Together AI key at: https://api.together.xyz/
Get a **free** Gemini key at: https://aistudio.google.com/app/apikey

---

### Step 4 — Start FastAPI Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
# API running at http://localhost:8000
```

Verify:
```bash
curl http://localhost:8000/health
# {"status":"connected","endee_url":"...","resume_index":"recruitiq_resumes",...}
```

---

### Step 5 — Start React Frontend

```bash
cd recruitiq-ui
npm install
npm run dev
# Opens at http://localhost:5173
```

---

### Step 6 — (Optional) Start Streamlit UI

```bash
cd endee/recruitiq
pip install -r requirements.txt
streamlit run app.py
# Opens at http://localhost:8501
```

---

### Step 7 — (Optional) Full Docker Compose

Run everything with one command:

```bash
# Copy and fill in your API key first
cp .env.example .env

# Start Endee + FastAPI together
docker-compose up -d
```

---

## 🧪 Verify Full Connection

```
1. http://localhost:8080/api/v1/indexes  → Endee DB health check
2. http://localhost:8000/health          → FastAPI + Endee status
3. http://localhost:5173                 → React UI (cinematic)
4. http://localhost:8501                 → Streamlit UI (optional)
```

---

## 📡 API Reference

### `GET /health`
Returns Endee connection status and index statistics.
```json
{
  "status": "connected",
  "endee_url": "http://localhost:8080/api/v1",
  "resume_index": "recruitiq_resumes",
  "resume_vector_count": 42,
  "embed_dim": 1024,
  "precision": "INT8D"
}
```

### `POST /upload`
Upload a single PDF resume for ingestion.
- Form field: `file` (PDF)
- Returns: `{ "status": "indexed", "id": "...", "name": "...", "skills_found": 8 }`

### `POST /upload/bulk`
Upload multiple PDF resumes at once.
- Form field: `files[]` (PDFs)

### `POST /search`
Run full RAG pipeline against uploaded resumes.
```json
{
  "jd": "Looking for a Python ML engineer with PyTorch experience...",
  "required_skills": ["python", "pytorch", "docker"],
  "min_exp": 2,
  "top_k": 8
}
```
Returns ranked candidates with composite scores + AI analysis per candidate.

---

## ⚙️ How Endee Vector DB Is Used

| Operation | Endee API Call | Purpose |
|-----------|---------------|---------|
| Index creation | `client.create_index()` | `recruitiq_resumes` + `recruitiq_jds`, cosine, INT8D |
| Resume storage | `client.upsert()` | Store 1024-dim embeddings + flat metadata |
| Semantic search | `client.search()` | Top-K cosine similarity retrieval |
| Filtered search | `search(filters={"years_exp": {"$gte": N}})` | Experience-gated retrieval |
| Index stats | `client.list_indexes()` | Dashboard health monitoring |

### Why Endee over Pinecone / Qdrant?
- **HNSW + INT8D quantization** — 4× less memory, same recall quality
- **Sub-5ms** query latency at scale
- **Docker-first, self-hostable** — no vendor lock-in, no cloud bills
- **Built-in metadata filtering** — no extra infrastructure needed
- **Open-source** — auditable, forkable, community-backed

---

## 🧠 RAG Pipeline Architecture

```
Job Description (text)
        │
        ▼
  [embedder.py]
  OpenAI-compat API → 1024-dim vector
        │
        ▼
  [endee_client.py]
  Endee HNSW Search (cosine, INT8D)
  Top-K candidates with metadata
        │
        ▼
  [agent.py — score_candidate()]
  Composite Score:
    50% semantic + 35% skill match + 15% exp
        │
        ▼
  [agent.py — screen_candidate()]
  LLM → Recommendation + Hire Reason
       + Concern + Interview Questions
        │
        ▼
  React Frontend — Ranked Candidate Cards
```

---

## 🧠 Challenges Faced

- Resolving pydantic v1/v2 conflicts between `endee` SDK and FastAPI
- Connecting Endee inside Docker Compose (service hostname vs localhost)
- Implementing INT8D quantization with correct cosine index parameters
- Designing flat metadata schema (Endee requires non-nested values)
- Building a fully responsive cinematic Three.js + glassmorphism UI
- Making the RAG pipeline gracefully degrade when backend is offline
- Handling PDF extraction edge cases (scanned PDFs, encoding issues)

---

## 📌 Future Enhancements

- 🔐 JWT-based recruiter authentication
- 📧 Automated candidate shortlisting via email
- 📊 Analytics dashboard (index growth, query latency charts)
- 🌍 Multi-language resume support (leveraging multilingual-e5)
- 📱 Mobile-responsive UI
- 🔄 Real-time re-ranking via WebSocket stream
- 🤖 Resume anonymization for bias-free hiring
- 📦 Kubernetes deployment manifests

---

## 🏁 Conclusion

**RecruitIQ** demonstrates the power of combining a **self-hosted open-source vector database** (Endee) with a modern **RAG pipeline** for a real-world hiring intelligence system.

The platform integrates **semantic vector search**, **composite AI scoring**, and **LLM-generated candidate analysis** — all packaged in a visually stunning, production-ready frontend.

It is scalable, extensible, and suitable for **real-world deployment or hackathon demonstration**.

---

## 🧑‍💻 Author

**Dhanush G**
Pre Final-Year Engineering Student
RecruitIQ — AI Resume Screening with Endee Vector DB

**Vector DB:** [endee.io](https://endee.io) | **Discord:** [discord.gg/5HFGqDZQE3](https://discord.gg/5HFGqDZQE3)
**GitHub:** [Dhanush-leet/RecuritIQ_Endee_Project](https://github.com/Dhanush-leet/RecuritIQ_Endee_Project)
