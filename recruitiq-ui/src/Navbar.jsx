import { motion } from 'framer-motion';
import { Menu, Zap } from 'lucide-react';

export default function Navbar() {
  return (
    <motion.nav 
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className="fixed top-0 left-0 w-full z-50 px-8 py-6 flex justify-between items-center pointer-events-none"
    >
      <div className="flex items-center gap-6 pointer-events-auto">
        <div className="flex flex-col">
          <span className="text-white font-bold tracking-[0.3em] text-xs">RECRUITIQ</span>
          <span className="mono-small">ENDURANCE MISSION : DAY 01</span>
        </div>
      </div>

      <div className="flex items-center gap-8 pointer-events-auto">
        <div className="hidden md:flex items-center gap-1">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="mono-small">SYSTEMS NOMINAL</span>
        </div>
        
        <button className="glass-card px-5 py-2 rounded-full border border-white/10 hover:border-white/30 transition-all group pointer-events-auto">
            <div className="flex items-center gap-3">
                <span className="mono-small opacity-100 group-hover:text-space-accent transition-colors">MENU</span>
                <Menu size={16} className="text-white/70" />
            </div>
        </button>
      </div>
    </motion.nav>
  );
}
