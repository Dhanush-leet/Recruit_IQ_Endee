import { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Briefcase, MapPin, ChevronRight, Search,
    Cpu, ArrowDown, Volume2, Shield, Zap,
    Upload, CheckCircle, XCircle, AlertCircle, ChevronDown, ChevronUp
} from 'lucide-react';
import CandidateRadar from './CandidateRadar';

const MOCK_CANDIDATES = [
  {
    id: 1,
    name: 'Eleanor Vance',
    role: 'Senior Machine Learning Engineer',
    location: 'San Francisco, CA',
    score: 98,
    semantic_score: 95,
    skill_match: 100,
    exp_score: 96,
    skills: ['python', 'pytorch', 'tensorflow', 'cuda', 'mlops'],
    matched_skills: ['python', 'pytorch', 'tensorflow'],
    missing_skills: [],
    years_exp: 8,
    ai_analysis: {
      recommendation: 'STRONG FIT',
      hire_reason: 'Exceptional deep learning background with 8 years of hands-on experience. PyTorch and CUDA expertise directly maps to production ML infrastructure needs.',
      concern: 'May be over-qualified for early-startup scaling phase.',
      interview_questions: [
        'Describe your experience optimizing CUDA kernels for production.',
        'How have you built MLOps pipelines at scale?',
        'Walk us through a model deployment that went wrong and how you fixed it.',
      ]
    }
  },
  {
    id: 2,
    name: 'Marcus Chen',
    role: 'Data Scientist',
    location: 'Remote (New York)',
    score: 92,
    semantic_score: 88,
    skill_match: 85,
    exp_score: 60,
    skills: ['python', 'sql', 'scikit-learn', 'aws', 'nlp'],
    matched_skills: ['python', 'sql', 'nlp'],
    missing_skills: ['docker'],
    years_exp: 5,
    ai_analysis: {
      recommendation: 'GOOD FIT',
      hire_reason: 'Strong NLP and cloud skills. AWS experience adds valuable infrastructure knowledge for ML deployment.',
      concern: 'Lacks Docker/containerization experience — needs ramp-up time.',
      interview_questions: [
        'How do you handle imbalanced datasets in production?',
        'Describe your experience with AWS SageMaker.',
        'How would you containerize an ML model for the first time?',
      ]
    }
  },
  {
    id: 3,
    name: 'Sophia Patel',
    role: 'AI Researcher',
    location: 'London, UK',
    score: 87,
    semantic_score: 82,
    skill_match: 75,
    exp_score: 48,
    skills: ['python', 'jax', 'transformers', 'c++', 'research'],
    matched_skills: ['python', 'transformers'],
    missing_skills: ['mlops', 'aws'],
    years_exp: 4,
    ai_analysis: {
      recommendation: 'PARTIAL FIT',
      hire_reason: 'Strong transformer architecture knowledge and research publication track record shows theoretical depth.',
      concern: 'Limited production/MLOps experience — better suited for research roles.',
      interview_questions: [
        'How have you translated research findings into production systems?',
        'Describe your experience with JAX vs PyTorch tradeoffs.',
        'What cloud platforms have you used for large-scale training?',
      ]
    }
  }
];

const REC_COLORS = {
  'STRONG FIT':  { bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', text: 'text-emerald-400', icon: CheckCircle },
  'GOOD FIT':    { bg: 'bg-blue-500/10',    border: 'border-blue-500/30',    text: 'text-blue-400',    icon: CheckCircle },
  'PARTIAL FIT': { bg: 'bg-yellow-500/10',  border: 'border-yellow-500/30',  text: 'text-yellow-400',  icon: AlertCircle },
  'NOT FIT':     { bg: 'bg-red-500/10',     border: 'border-red-500/30',     text: 'text-red-400',     icon: XCircle    },
};

export default function Home() {
    const [isSearching, setIsSearching]   = useState(false);
    const [candidates,  setCandidates]    = useState([]);
    const [showApp,     setShowApp]       = useState(false);
    const [expandedCard, setExpandedCard] = useState(null);
    const [uploadStatus, setUploadStatus] = useState(null); // {name, status}
    const [dbConnected,  setDbConnected]  = useState(null); // true/false/null
    const fileRef = useRef(null);

    // ── Check backend health on mount ────────────────────────────
    const checkHealth = async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/health');
            const d   = await res.json();
            setDbConnected(d.endee_status === 'online');
        } catch {
            setDbConnected(false);
        }
    };

    // ── Upload resume PDF ─────────────────────────────────────────
    const handleUpload = async (file) => {
        if (!file || !file.name.endsWith('.pdf')) return;
        setUploadStatus({ name: file.name, status: 'uploading' });
        const form = new FormData();
        form.append('file', file);
        try {
            const res  = await fetch('http://127.0.0.1:8000/upload', { method: 'POST', body: form });
            const data = await res.json();
            setUploadStatus({ name: data.name || file.name, status: 'done', skills: data.skills_found });
        } catch {
            setUploadStatus({ name: file.name, status: 'error' });
        }
    };

    // ── RAG Search ───────────────────────────────────────────────
    const handleSearch = async (queryText, minExp = 0) => {
        if (!queryText.trim()) return;
        setIsSearching(true);
        try {
            const res = await fetch('http://127.0.0.1:8000/search', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    jd:               queryText,
                    required_skills:  [],
                    min_exp:          minExp,
                    top_k:            8,
                }),
            });
            const data = await res.json();
            setCandidates(data.candidates?.length ? data.candidates : MOCK_CANDIDATES);
        } catch {
            setCandidates(MOCK_CANDIDATES);
        } finally {
            setIsSearching(false);
        }
    };

    const handleStart = () => {
        setShowApp(true);
        checkHealth();
        handleSearch('Senior Machine Learning Engineer');
    };

    return (
        <div className="relative z-20 w-full min-h-screen text-white overflow-y-auto no-scrollbar">

            {/* ── Landing Hero ────────────────────────────────────── */}
            <AnimatePresence>
            {!showApp && (
                <motion.div
                    exit={{ opacity: 0, scale: 1.08, filter: 'blur(20px)' }}
                    transition={{ duration: 1.4, ease: 'easeInOut' }}
                    className="min-h-screen flex flex-col items-center justify-center px-6 text-center"
                >
                    <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4, duration: 1 }}>
                        <span className="mono-small mb-4 block tracking-[0.5em] text-space-accent">ENDEE VECTOR INTELLIGENCE</span>
                        <h1 className="text-6xl md:text-[8rem] font-extralight tracking-[-0.04em] mb-6 text-glow text-gradient leading-none">
                            RECRUIT<span className="font-bold">IQ</span>
                        </h1>
                        <p className="max-w-lg mx-auto text-white/40 text-lg font-light mb-4 leading-relaxed">
                            Semantic resume matching powered by Endee's HNSW vector engine —
                            STRONG FIT candidates surfaced in milliseconds.
                        </p>
                        <div className="flex items-center justify-center gap-6 mb-12 text-[11px] font-mono text-white/30">
                            <span>HNSW + INT8D</span>
                            <span className="w-1 h-1 rounded-full bg-white/20"/>
                            <span>1024-DIM VECTORS</span>
                            <span className="w-1 h-1 rounded-full bg-white/20"/>
                            <span>RAG PIPELINE</span>
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.04 }}
                            whileTap={{ scale: 0.97 }}
                            onClick={handleStart}
                            className="relative glass-card px-12 py-5 rounded-full text-white font-mono text-sm tracking-widest border border-white/20 overflow-hidden group"
                        >
                            INITIATE ANALYSIS
                            <div className="absolute inset-0 bg-gradient-to-r from-space-accent/25 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-[900ms]" />
                        </motion.button>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0 }} animate={{ opacity: 0.4 }} transition={{ delay: 1.8, duration: 1 }}
                        className="absolute bottom-10 flex flex-col items-center gap-2"
                    >
                        <span className="mono-small">ENDEE PROTOCOL v2.0</span>
                        <ArrowDown size={15} className="animate-bounce" />
                    </motion.div>
                </motion.div>
            )}
            </AnimatePresence>

            {/* ── Main App ─────────────────────────────────────────── */}
            {showApp && (
                <motion.div
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.9, delay: 0.3 }}
                    className="max-w-6xl mx-auto px-6 py-28"
                >
                    {/* Header row */}
                    <div className="flex flex-col md:flex-row justify-between items-end gap-6 mb-14">
                        <div>
                            <span className="mono-small text-space-accent mb-2 block">ENDEE SEMANTIC SEARCH</span>
                            <h2 className="text-4xl md:text-5xl font-light">Candidate Radar</h2>
                        </div>

                        <div className="flex items-center gap-3">
                            {/* DB Status pill */}
                            <div className={`glass-card px-5 py-2.5 rounded-2xl flex items-center gap-3 border ${dbConnected === true ? 'border-emerald-500/30' : dbConnected === false ? 'border-red-500/30' : 'border-white/10'}`}>
                                <div className={`w-2 h-2 rounded-full animate-pulse ${dbConnected === true ? 'bg-emerald-400' : dbConnected === false ? 'bg-red-400' : 'bg-white/30'}`} />
                                <div className="flex flex-col">
                                    <span className="mono-small !text-[9px] !opacity-40">ENDEE STATUS</span>
                                    <span className={`text-xs font-mono ${dbConnected === true ? 'text-emerald-400' : dbConnected === false ? 'text-red-400' : 'text-white/40'}`}>
                                        {dbConnected === true ? 'CONNECTED' : dbConnected === false ? 'OFFLINE' : 'CHECKING...'}
                                    </span>
                                </div>
                            </div>

                            {/* Upload button */}
                            <button
                                onClick={() => fileRef.current?.click()}
                                className="glass-card px-5 py-2.5 rounded-2xl flex items-center gap-2 text-xs font-mono text-white/50 hover:text-white hover:bg-white/5 border border-white/10 transition-all"
                            >
                                <Upload size={14} />
                                UPLOAD PDF
                            </button>
                            <input ref={fileRef} type="file" accept=".pdf" className="hidden" onChange={e => handleUpload(e.target.files[0])} />
                        </div>
                    </div>

                    {/* Upload status toast */}
                    <AnimatePresence>
                    {uploadStatus && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                            className={`mb-6 p-4 rounded-2xl border text-sm font-mono flex items-center gap-3 ${
                                uploadStatus.status === 'done'      ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                              : uploadStatus.status === 'uploading' ? 'bg-white/5 border-white/10 text-white/60'
                              : 'bg-red-500/10 border-red-500/30 text-red-400'
                            }`}
                        >
                            {uploadStatus.status === 'done'      ? <CheckCircle size={16} /> :
                             uploadStatus.status === 'uploading' ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> :
                             <XCircle size={16} />}
                            {uploadStatus.status === 'done'
                                ? `✅ "${uploadStatus.name}" indexed into Endee — ${uploadStatus.skills} skills extracted`
                                : uploadStatus.status === 'uploading'
                                ? `Ingesting "${uploadStatus.name}" into Endee vector DB...`
                                : `Failed to upload — is the backend running on port 8000?`}
                        </motion.div>
                    )}
                    </AnimatePresence>

                    {/* Search bar */}
                    <div className="glass-card p-2 rounded-3xl mb-14 focus-within:ring-1 ring-space-accent/50 transition-all duration-500">
                        <div className="flex flex-col md:flex-row items-center">
                            <div className="flex-1 flex items-center px-6 py-4">
                                <Search className="text-white/20 mr-4 shrink-0" size={20} />
                                <input
                                    type="text"
                                    id="jdInput"
                                    placeholder="Paste job description or type a role to find best candidates..."
                                    className="w-full bg-transparent border-none text-white focus:outline-none text-lg font-light placeholder:text-white/20"
                                    onKeyDown={(e) => e.key === 'Enter' && handleSearch(e.target.value)}
                                />
                            </div>
                            <button
                                onClick={() => handleSearch(document.getElementById('jdInput').value)}
                                className="bg-white text-black px-10 py-5 rounded-[1.4rem] font-bold text-sm tracking-widest hover:bg-space-accent hover:text-white transition-all duration-300 m-1 shrink-0"
                            >
                                EXECUTE RAG
                            </button>
                        </div>
                    </div>

                    {/* Results */}
                    <div className="grid grid-cols-1 gap-5">
                        {isSearching ? (
                            [1,2,3].map(i => (
                                <div key={i} className="h-56 glass-card rounded-3xl animate-pulse shimmer" />
                            ))
                        ) : candidates.map((c, i) => {
                            const rec    = c.ai_analysis?.recommendation || 'PARTIAL FIT';
                            const colors = REC_COLORS[rec] || REC_COLORS['PARTIAL FIT'];
                            const RecIcon = colors.icon;
                            const open   = expandedCard === c.id;

                            return (
                                <motion.div
                                    key={c.id || i}
                                    initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: i * 0.07 }}
                                    className={`glass-card p-8 rounded-3xl border transition-all relative overflow-hidden ${open ? 'border-space-accent/30' : 'border-white/5 hover:border-white/15'}`}
                                >
                                    {/* Score badge */}
                                    <div className="absolute top-6 right-6 flex flex-col items-end gap-0.5">
                                        <span className="mono-small !text-[9px] !opacity-30">COMPOSITE SCORE</span>
                                        <span className="text-5xl font-extralight text-space-accent leading-none">{c.score}</span>
                                    </div>

                                    {/* Main row */}
                                    <div className="flex flex-col md:flex-row gap-7 items-start pr-24">

                                        {/* Avatar + radar */}
                                        <div className="flex flex-col items-center gap-3 shrink-0">
                                            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-white/10 to-transparent flex items-center justify-center border border-white/10 group-hover:scale-105 transition-transform">
                                                <Cpu size={36} className="text-white/35" />
                                            </div>
                                            <CandidateRadar score={c.score} />
                                        </div>

                                        {/* Info */}
                                        <div className="flex-1 min-w-0">
                                            <div className="flex flex-wrap items-center gap-2 mb-1">
                                                <h3 className="text-2xl font-light">{c.name}</h3>
                                                <span className={`px-2 py-0.5 rounded border text-[10px] font-mono flex items-center gap-1 ${colors.bg} ${colors.border} ${colors.text}`}>
                                                    <RecIcon size={10} /> {rec}
                                                </span>
                                            </div>

                                            <div className="flex flex-wrap gap-4 mb-5 text-white/40 text-[13px]">
                                                <span className="flex items-center gap-1.5"><Briefcase size={13} className="text-space-accent/70"/> {c.role || 'Engineer'}</span>
                                                <span className="flex items-center gap-1.5"><MapPin    size={13} className="text-space-accent/70"/> {c.location || 'Remote'}</span>
                                                <span className="flex items-center gap-1.5"><Zap       size={13} className="text-space-accent/70"/> {c.years_exp || 0} yrs exp</span>
                                            </div>

                                            {/* Score breakdown */}
                                            <div className="grid grid-cols-3 gap-3 mb-5">
                                                {[
                                                    { label: 'SEMANTIC',    val: c.semantic_score ?? '—' },
                                                    { label: 'SKILL MATCH', val: c.skill_match    ?? '—' },
                                                    { label: 'EXPERIENCE',  val: c.exp_score      ?? '—' },
                                                ].map(({ label, val }) => (
                                                    <div key={label} className="bg-white/[0.03] border border-white/5 rounded-xl p-3">
                                                        <div className="mono-small !text-[9px] !opacity-30 mb-1">{label}</div>
                                                        <div className="text-lg font-light">{typeof val === 'number' ? `${val}%` : val}</div>
                                                    </div>
                                                ))}
                                            </div>

                                            {/* Skills chips */}
                                            <div className="flex flex-wrap gap-2">
                                                {(c.skills || []).slice(0, 8).map(s => (
                                                    <span key={s} className={`px-3 py-1 rounded-full text-[10px] font-mono border transition-colors ${
                                                        (c.matched_skills || []).map(m => m.toLowerCase()).includes(s.toLowerCase())
                                                            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                                                            : 'bg-white/5 border-white/5 text-white/40'
                                                    }`}>{s}</span>
                                                ))}
                                                {(c.missing_skills || []).map(s => (
                                                    <span key={s} className="px-3 py-1 bg-red-500/10 border border-red-500/20 rounded-full text-[10px] font-mono text-red-400/80">
                                                        ✗ {s}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>

                                        {/* Action buttons */}
                                        <div className="flex flex-col gap-2 shrink-0 min-w-[150px]">
                                            <button className="bg-white text-black px-6 py-3 rounded-xl text-xs font-bold tracking-widest hover:bg-space-accent hover:text-white transition-all flex items-center justify-center gap-2">
                                                VIEW PROFILE <ChevronRight size={13} />
                                            </button>
                                            <button
                                                onClick={() => setExpandedCard(open ? null : c.id || i)}
                                                className="glass-card px-6 py-3 rounded-xl text-xs font-mono tracking-widest text-white/50 hover:text-white hover:bg-white/5 transition-all flex items-center justify-center gap-2"
                                            >
                                                {open ? <><ChevronUp size={13}/> CLOSE</> : <><ChevronDown size={13}/> RAG ANALYSIS</>}
                                            </button>
                                        </div>
                                    </div>

                                    {/* ── Expandable AI analysis panel ── */}
                                    <AnimatePresence>
                                    {open && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: 'auto', opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                            transition={{ duration: 0.35 }}
                                            className="overflow-hidden"
                                        >
                                            <div className="mt-8 pt-8 border-t border-white/10 grid grid-cols-1 md:grid-cols-2 gap-8">
                                                <div>
                                                    <h4 className="mono-small text-white/40 mb-4">AI HIRE REASON</h4>
                                                    <p className="text-sm text-white/70 leading-relaxed italic">
                                                        "{c.ai_analysis?.hire_reason}"
                                                    </p>
                                                    {c.ai_analysis?.concern && (
                                                        <p className="mt-3 text-xs text-yellow-400/70 flex gap-2">
                                                            <AlertCircle size={12} className="mt-0.5 shrink-0" />
                                                            {c.ai_analysis.concern}
                                                        </p>
                                                    )}
                                                </div>
                                                <div>
                                                    <h4 className="mono-small text-white/40 mb-4">SUGGESTED INTERVIEW QUESTIONS</h4>
                                                    <ol className="space-y-2">
                                                        {(c.ai_analysis?.interview_questions || []).map((q, qi) => (
                                                            <li key={qi} className="text-xs text-white/55 flex gap-2 leading-snug">
                                                                <span className="text-space-accent font-mono shrink-0">{qi + 1}.</span>
                                                                {q}
                                                            </li>
                                                        ))}
                                                    </ol>
                                                    <div className="mt-5 flex gap-6 text-[11px]">
                                                        <div>
                                                            <div className="mono-small !text-[9px] mb-1">ENDEE VEC ID</div>
                                                            <div className="font-mono text-white/30">{c.id || `IDX_R-${i+1}`}</div>
                                                        </div>
                                                        <div>
                                                            <div className="mono-small !text-[9px] mb-1">PRIORITY</div>
                                                            <div className={`font-bold uppercase ${colors.text}`}>
                                                                {rec === 'STRONG FIT' ? 'High' : rec === 'GOOD FIT' ? 'Medium' : 'Low'}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </motion.div>
                                    )}
                                    </AnimatePresence>
                                </motion.div>
                            );
                        })}
                    </div>
                </motion.div>
            )}

            {/* ── Footer status bar ──────────────────────────────── */}
            <div className="fixed bottom-7 left-7 z-50 flex items-center gap-3 pointer-events-none">
                <div className="w-9 h-9 glass-card rounded-full flex items-center justify-center pointer-events-auto cursor-pointer hover:bg-white/10 transition-all">
                    <Volume2 size={15} className="text-white/35" />
                </div>
                <div className="p-3 glass-card rounded-xl flex items-center gap-2.5 pointer-events-auto border border-space-accent/15">
                    <Shield size={13} className="text-space-accent" />
                    <span className="mono-small !opacity-100 !text-white/50">ENDEE VECTOR NODE · PORT 8080</span>
                </div>
            </div>
        </div>
    );
}
