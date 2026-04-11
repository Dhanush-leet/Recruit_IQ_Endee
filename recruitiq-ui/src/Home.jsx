import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    Briefcase, MapPin, Star, Sparkles, ChevronRight, Search, 
    FileText, Cpu, Globe, ArrowDown, Volume2, Shield, Zap
} from 'lucide-react';
import CandidateRadar from './CandidateRadar';

const MOCK_CANDIDATES = [
  {
    id: 1,
    name: 'Eleanor Vance',
    role: 'Senior Machine Learning Engineer',
    location: 'San Francisco, CA',
    score: 98,
    skills: ['Python', 'PyTorch', 'TensorFlow', 'CUDA', 'MLOps'],
    match: 'Strong Fit',
    exp: '8 years',
    fitReason: 'Exceptional background in deep learning infrastructure and large language models.'
  },
  {
    id: 2,
    name: 'Marcus Chen',
    role: 'Data Scientist',
    location: 'Remote (New York)',
    score: 92,
    skills: ['Python', 'SQL', 'Scikit-Learn', 'AWS', 'NLP'],
    match: 'Good Fit',
    exp: '5 years',
    fitReason: 'Strong foundation in natural language processing and AWS cloud architecture.'
  },
  {
    id: 3,
    name: 'Sophia Patel',
    role: 'AI Researcher',
    location: 'London, UK',
    score: 87,
    skills: ['Python', 'JAX', 'Transformers', 'C++', 'Research'],
    match: 'Good Fit',
    exp: '4 years',
    fitReason: 'Impressive publication record and experience with transformer architectures.'
  }
];

export default function Home() {
    const [isSearching, setIsSearching] = useState(false);
    const [candidates, setCandidates] = useState([]);
    const [showApp, setShowApp] = useState(false);
    
    const handleSearch = async (queryText) => {
        if (!queryText) return;
        setIsSearching(true);
        try {
            const formData = new FormData();
            formData.append("query", queryText);
            
            const response = await fetch("http://localhost:8000/search", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            setCandidates(data);
        } catch (error) {
            console.error("Backend offline, using fallback data");
            setCandidates(MOCK_CANDIDATES);
        } finally {
            setIsSearching(false);
        }
    };

    const handleStart = () => {
        setShowApp(true);
        handleSearch("Senior Machine Learning Engineer");
    };

  return (
    <div className="relative z-20 w-full min-h-screen text-white overflow-y-auto no-scrollbar">
        
        {/* Landing Hero Section */}
        <AnimatePresence>
        {!showApp && (
            <motion.div 
                exit={{ opacity: 0, scale: 1.1, filter: "blur(20px)" }}
                transition={{ duration: 1.5, ease: "easeInOut" }}
                className="min-h-screen flex flex-col items-center justify-center px-6 text-center"
            >
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5, duration: 1 }}
                >
                    <span className="mono-small mb-4 block tracking-[0.5em] text-space-accent">ORBITAL ENTRY</span>
                    <h1 className="text-6xl md:text-9xl font-extralight tracking-tighter mb-8 text-gradient">
                        RECRUIT<span className="font-bold">IQ</span>
                    </h1>
                    <p className="max-w-xl mx-auto text-white/40 text-lg md:text-xl font-light mb-12 leading-relaxed">
                        A proprietary intelligence layer for elite technical recruitment. 
                        Powered by Endee's semantic architecture.
                    </p>
                    
                    <motion.button 
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleStart}
                        className="glass-card px-10 py-5 rounded-full text-white font-mono text-sm tracking-widest hover:bg-white/10 transition-all border border-white/20 group"
                    >
                        INITIATE ANALYSIS
                        <div className="absolute inset-0 rounded-full border border-space-accent/50 scale-110 opacity-0 group-hover:opacity-100 group-hover:scale-100 transition-all duration-300" />
                    </motion.button>
                </motion.div>

                <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 0.5 }}
                    transition={{ delay: 1.5, duration: 1 }}
                    className="absolute bottom-12 flex flex-col items-center gap-2"
                >
                    <span className="mono-small">SCROLL TO EXPLORE</span>
                    <ArrowDown size={16} className="animate-bounce" />
                </motion.div>
            </motion.div>
        )}
        </AnimatePresence>

        {/* Main Application Section */}
        {showApp && (
            <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 1, delay: 0.5 }}
                className="max-w-6xl mx-auto px-6 py-32"
            >
                <div className="flex flex-col md:flex-row justify-between items-end gap-8 mb-16">
                    <div>
                        <span className="mono-small text-space-accent mb-2 block">SEARCH PARAMETERS</span>
                        <h2 className="text-4xl md:text-5xl font-light">Candidate Radar</h2>
                    </div>
                    
                    <div className="flex gap-4">
                        <div className="glass-card px-6 py-3 rounded-2xl flex items-center gap-4">
                            <div className="flex flex-col">
                                <span className="mono-small !opacity-30">DATABASE STATUS</span>
                                <span className="text-sm font-mono text-emerald-400">ENDEE : ONLINE</span>
                            </div>
                            <Cpu size={24} className="text-white/20" />
                        </div>
                    </div>
                </div>

                <div className="glass-card p-2 rounded-3xl mb-16 focus-within:ring-1 ring-space-accent/50 transition-all duration-500">
                    <div className="flex flex-col md:flex-row items-center">
                        <div className="flex-1 flex items-center px-6 py-4">
                            <Search className="text-white/20 mr-4" size={20} />
                            <input 
                                type="text" 
                                id="jdInput"
                                placeholder="Paste job description or search roles..."
                                className="w-full bg-transparent border-none text-white focus:outline-none text-lg font-light placeholder:text-white/20"
                            />
                        </div>
                        <button 
                            onClick={() => handleSearch(document.getElementById('jdInput').value)}
                            className="bg-white text-black px-10 py-5 rounded-[1.4rem] font-bold text-sm tracking-widest hover:bg-space-accent hover:text-white transition-all duration-300 m-1">
                            EXECUTE RAG
                        </button>
                    </div>
                </div>

                {/* Results Grid */}
                <div className="grid grid-cols-1 gap-6">
                    {isSearching ? (
                        [1,2,3].map(i => (
                            <div key={i} className="h-40 glass-card rounded-3xl animate-pulse shimmer" />
                        ))
                    ) : (
                        candidates.map((candidate, i) => (
                            <motion.div
                                key={candidate.id}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: i * 0.1 }}
                                className="glass-card p-8 rounded-3xl border border-white/5 hover:border-white/20 transition-all group relative overflow-hidden"
                            >
                                <div className="absolute top-0 right-0 p-6">
                                    <div className="flex flex-col items-end">
                                        <span className="text-4xl font-extralight text-space-accent">{candidate.score}</span>
                                        <span className="mono-small">MATCH INDEX</span>
                                    </div>
                                </div>

                                <div className="flex flex-col md:flex-row gap-8 items-start md:items-center">
                                    <div className="flex items-center gap-4">
                                        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-white/10 to-transparent flex items-center justify-center border border-white/10">
                                            <Cpu size={32} className="text-white/40" />
                                        </div>
                                        <CandidateRadar score={candidate.score} />
                                    </div>
                                    
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-1">
                                            <h3 className="text-2xl font-light">{candidate.name}</h3>
                                            <div className="px-2 py-0.5 rounded border border-emerald-500/30 bg-emerald-500/10 text-[10px] text-emerald-400 font-mono">ACTIVE</div>
                                        </div>
                                        <div className="flex flex-wrap gap-4 mb-4 text-white/40 text-sm">
                                            <span className="flex items-center gap-1"><Briefcase size={14}/>{candidate.role}</span>
                                            <span className="flex items-center gap-1"><MapPin size={14}/>{candidate.location}</span>
                                            <span className="flex items-center gap-1"><Zap size={14}/>{candidate.exp}</span>
                                        </div>
                                        <div className="flex flex-wrap gap-2">
                                            {candidate.skills.map(s => (
                                                <span key={s} className="px-3 py-1 bg-white/5 rounded-full text-[11px] font-mono border border-white/5 text-white/60">{s}</span>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="flex flex-col gap-2">
                                        <button className="glass-card px-6 py-3 rounded-xl text-xs font-mono tracking-widest hover:bg-white/10 transition-all flex items-center gap-2">
                                            VIEW PROFILE <ChevronRight size={14} />
                                        </button>
                                        <button className="px-6 py-3 rounded-xl text-xs font-mono tracking-widest text-white/30 hover:text-white transition-all">
                                            AI SUMMARY
                                        </button>
                                    </div>
                                </div>
                            </motion.div>
                        ))
                    )}
                </div>
            </motion.div>
        )}

        {/* Global Footer Elements */}
        <div className="fixed bottom-8 left-8 z-50 flex items-center gap-4 pointer-events-none">
            <div className="w-10 h-10 glass-card rounded-full flex items-center justify-center pointer-events-auto cursor-pointer hover:bg-white/10 transition-all">
                <Volume2 size={16} className="text-white/40" />
            </div>
            <div className="p-3 glass-card rounded-xl flex items-center gap-3 pointer-events-auto">
                <Shield size={14} className="text-space-accent" />
                <span className="mono-small !opacity-100 !text-white/60">SECURE NODE 72.0</span>
            </div>
        </div>
    </div>
  );
}
