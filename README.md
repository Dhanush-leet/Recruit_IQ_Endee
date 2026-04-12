# **RECRUITIQ: AI-POWERED RESUME SCREENING & SEMANTIC MATCHING PORTAL**

**A Full-Stack AI Hiring platform powered by Endee Vector Database, RAG, and Cinematic UI**

---

## 📌 Overview

**RecruitIQ** is a complete **full-stack AI resume screening and semantic matching platform** built using **React (Vite) + Three.js** for the cinematic frontend and **FastAPI** for the backend, with **Endee** as the open-source vector database.

This application enables recruiters to **ingest PDF resumes**, perform **semantic search** using job descriptions, calculate **composite match scores**, generate **AI-driven screening insights**, and identify **skill gaps** using real-time RAG processing.

The platform is designed to be:

* 🔐 Secure & Private
* ⚡ Ultra-Fast 
* 📊 Data-driven
* 🎯 Highly Accurate

It is ideal for **recruiters, HR tech professionals, and AI application developers**.

---

## 🖥️ Tech Stack

### Frontend

* React (Vite)
* Tailwind CSS
* Framer Motion (Cinematic Animations)
* Three.js (Particle Backgrounds)
* Axios

### Backend

* Python (FastAPI)
* RESTful APIs
* Endee Python SDK (`endee>=0.1.25`)
* PyMuPDF (PDF Extraction)
* OpenAI-Compatible LLM APIs (Together AI / Gemini)

### Database (Vector)

* Endee OSS Vector Database (HNSW, INT8D Quantization, Cosine Similarity)

### Deployment

* Frontend: **Vite Localhost / Vercel**
* Backend: **Docker / Localhost**
* Database: **Docker (Local)**

---

## 📂 Project Structure

```
RecuritIQ_Endee_Project/
│
├── recruitiq-ui/
│   ├── src/
│   │   ├── components/
│   │   ├── Home.jsx
│   │   ├── ParticleBackground.jsx
│   │   ├── CandidateRadar.jsx
│   │   └── App.css
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── agent.py
│   ├── config.py
│   ├── embedder.py
│   ├── endee_client.py
│   ├── ingest.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ✨ Key Features

### 🔐 Architecture & Security

* Self-hosted Endee Vector Database (No data leaves your local/AWS node unless required)
* Local PDF Extraction without cloud privacy risks
* API-key protected LLM integration
* Modular Microservices architecture

---

## 🏠 Landing Page

* Cinematic glassmorphism hero section
* 3D Three.js interactive particle background
* Live vector database connection status
* Entry point for uploading resumes and RAG search

---

## 📊 Recruitment Dashboard

* Semantic search input for raw Job Descriptions
* Comprehensive candidate radar charts
* High-level statistical breakdown of scores
* Toggle-able AI analysis per candidate

---

## 💼 PDF Resume Ingestion

### 🔹 Single Node Upload

* Direct PDF file selection
* Real-time text extraction via PyMuPDF
* Real-time metadata generation (Skills, Email, Experience)

### 🔹 Bulk Upload

* Batch ingestion capabilities
* Automated vectorization via Multilingual e5-large-instruct
* Direct HNSW-indexed storage on Endee DB

---

## 📈 Composite Scoring Engine

* **50% Semantic Score**: Pure cosine distance from the Endee vector search
* **35% Skill Match**: Keyword matching between job requirements and extracted candidate skills
* **15% Experience Score**: Normalized calculation based on years of experience

---

## 🧾 AI Screening (RAG) Module

* LLM-driven candidate profiling
* Actionable hiring recommendations: **STRONG FIT, GOOD FIT, PARTIAL FIT, NOT FIT**
* 2-3 sentence justifications tailored exactly to the JD
* Extractable JSON insights

---

## 🚨 Skill Gap & Risk Scanner

* Compares dynamically extracted skills against explicitly provided job constraints
* Live gap detection:
  * ✅ Present Skills → Identified and matched
  * ❌ Missing Skills → Flagged immediately as gaps
* Real-time concern flagging via the AI Agent layer

---

## ⚠️ Experience & Risk Analysis

### 🔹 Semantic Drift Risk

* Evaluates if a candidate is technically sound but conceptually off-base for a custom domain

### 🔹 Over-qualification / Under-qualification

* Uses the extracted years of experience against the LLM's understanding of the role seniority
* Immediate feedback for interview priority (High, Medium, Low)

---

## 📚 Technical Interview Generation

* LLM constructs 3 tailored interview questions per candidate
* Based strictly on the missing skills and the core requirements of the job description
* Helps non-technical recruiters interview deeply technical candidates

---

## ⚙️ Application Settings & Configuration

* Toggleable embeddings models (Together AI, Gemini, OpenAI)
* Configurable vector dimensions (768, 1024, 1536)
* Adjustable similarity algorithms and batch size through a simple `.env`

---

## 🧠 Challenges Faced

* Resolving dependency conflicts between Python SDKs
* Synchronizing the frontend application state with the live responses from the FastAPI backend
* Optimizing the Prompt Engineering (RAG) to ensure the LLM strictly returned parsable JSON structure without markdown fencing
* Configuring the Endee vector database correctly via Docker (mapping HNSW M/ef_con parameters)
* Designing flat metadata schemas suitable for rapid vector retrieval

---

## 🏁 Conclusion

This project demonstrates the successful development of a **Full-stack AI-Powered Recruitment System** using modern technologies and cutting-edge NLP patterns.
It integrates **real-time vector similarity search**, **advanced RAG analytics**, and **beautiful UX principles** to help recruiters make **informed, data-driven hiring decisions**.

The application is highly scalable, extensible, and suitable for **real-world HR-Tech enterprise integration or academic demonstration**.

---

## 📌 Future Enhancements

* Role-based Access Control (Recruiters vs Admins)
* Cloud-hosted Endee integration without Docker reliance
* AI-driven resume re-writing and anonymization
* Candidate communication system (automated rejection/advancement emails)
* WebSocket-based live ingestion progress updates

---

## 🧑‍💻 Author

**Dhanush**
Pre Final-Year Engineering Student
RecruitIQ – AI Resume Screening with Endee Vector DB

---
