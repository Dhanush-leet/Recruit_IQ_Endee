import streamlit as st
import tempfile, os, uuid
import plotly.graph_objects as go
from ingest.pdf_extractor import extract_resume_text, parse_resume_metadata
from ingest.embedder import embed, make_id
from ingest.uploader import setup_indexes, upsert_resume
from retrieval.matcher import find_matching_resumes
from retrieval.scorer import compute_skill_gap, combined_score
from generation.prompt_builder import build_screening_prompt
from generation.llm import get_screening_analysis

st.set_page_config(page_title="RecruitIQ", page_icon="🎯", layout="wide")
setup_indexes()

st.title("🎯 RecruitIQ — AI Resume Screener")
st.caption("Powered by Endee Vector Database · Semantic Search + RAG")

# ── Sidebar ──
with st.sidebar:
    st.header("📤 Upload Resumes")
    uploaded = st.file_uploader("Drop PDF resumes", type="pdf", accept_multiple_files=True)
    
    if uploaded and st.button("Ingest All Resumes", type="primary"):
        progress = st.progress(0)
        for i, f in enumerate(uploaded):
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(f.read())
                path = tmp.name
            text = extract_resume_text(path)
            meta = parse_resume_metadata(text, f.name)
            vec = embed(text[:1000])
            upsert_resume(make_id(f.name + text[:100]), vec, meta)
            os.unlink(path)
            progress.progress((i + 1) / len(uploaded))
        st.success(f"✅ {len(uploaded)} resumes ingested into Endee!")
    
    st.divider()
    st.header("⚙️ Filters")
    min_exp = st.slider("Min. years experience", 0, 15, 0)
    top_k = st.slider("Top candidates to retrieve", 3, 20, 8)

# ── Main Panel ──
tab1, tab2 = st.tabs(["🔍 Screen Candidates", "📊 Analytics"])

with tab1:
    jd_text = st.text_area("Paste Job Description here", height=180,
                            placeholder="We are looking for a Python developer with 3+ years experience in ML...")
    required_skills_input = st.text_input("Required skills (comma-separated)",
                                          "python, machine learning, sql, docker")
    
    if st.button("🚀 Find Best Candidates", type="primary", use_container_width=True):
        if not jd_text.strip():
            st.warning("Please enter a job description.")
        else:
            required_skills = [s.strip() for s in required_skills_input.split(",")]
            jd_vec = embed(jd_text)
            
            with st.spinner("Searching Endee vector index..."):
                results = find_matching_resumes(jd_vec, top_k=top_k, min_exp=min_exp)
            
            if not results:
                st.info("No candidates found. Upload some resumes first!")
            else:
                st.subheader(f"Top {len(results)} Candidates")
                
                for i, r in enumerate(results):
                    meta = r.get("metadata", {})
                    sem_score = r.get("score", 0)
                    gap = compute_skill_gap(required_skills, meta.get("skills", []))
                    exp_score = min(meta.get("years_exp", 0) / 10, 1.0)
                    final = combined_score(sem_score, gap["score"], exp_score)
                    
                    color = "🟢" if gap["match_pct"] >= 70 else ("🟡" if gap["match_pct"] >= 40 else "🔴")
                    
                    with st.expander(f"{color} #{i+1} — {meta.get('name','Unknown')} | Score: {round(final*100)}% | Match: {gap['match_pct']}%"):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Semantic Score", f"{round(sem_score*100)}%")
                        col2.metric("Skill Match", f"{gap['match_pct']}%")
                        col3.metric("Experience", f"{meta.get('years_exp',0)} yrs")
                        
                        if gap["matched"]:
                            st.success(f"✅ Matched skills: {', '.join(gap['matched'])}")
                        if gap["missing"]:
                            st.error(f"❌ Missing skills: {', '.join(gap['missing'])}")
                        
                        if st.button(f"🤖 AI Analysis for {meta.get('name','Candidate')}", key=f"ai_{i}"):
                            prompt = build_screening_prompt(
                                jd_text, meta.get("raw_text",""), gap, sem_score
                            )
                            with st.spinner("Generating AI screening report..."):
                                analysis = get_screening_analysis(prompt)
                            
                            rec = analysis.get("recommendation","")
                            badge = {"STRONG FIT":"🟢","GOOD FIT":"🔵","PARTIAL FIT":"🟡","NOT FIT":"🔴"}.get(rec,"⚪")
                            st.markdown(f"### {badge} {rec}")
                            st.markdown(f"**Why hire:** {analysis.get('hire_reason','')}")
                            st.markdown(f"**Concern:** {analysis.get('concern','')}")
                            qs = analysis.get("suggested_interview_questions",[])
                            if qs:
                                st.markdown("**Interview Questions:**")
                                for q in qs:
                                    st.markdown(f"- {q}")

with tab2:
    st.subheader("📊 Index Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Resumes in Endee", "—")
    col2.metric("JDs Indexed", "—")
    st.info("Upload resumes and run a search to see analytics populate.")
