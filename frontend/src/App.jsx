import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Upload,
  Activity,
  Heart,
  Wind,
  CheckCircle2,
  AlertCircle,
  Loader2,
  FileAudio,
  BarChart3,
  Stethoscope,
  Waves
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE_URL = 'http://localhost:8000';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

function App() {
  const [mode, setMode] = useState('heart');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResult(null);
      setError(null);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handlePredict = async () => {
    if (!file) {
      setError('Please select an audio file first.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = mode === 'heart' ? '/predict/heart' : '/predict/lung';
      const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'An unexpected error occurred. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-4 sm:p-8 font-sans">
      <div className="w-full max-w-6xl">
        {/* Navbar-style Header */}
        <header className="flex flex-col sm:flex-row items-center justify-between mb-12 space-y-4 sm:space-y-0">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-3"
          >
            <div className="bg-blue-600 p-2.5 rounded-2xl shadow-lg shadow-blue-500/20">
              <Activity className="text-white" size={28} />
            </div>
            <div>
              <h1 className="text-2xl font-black tracking-tight text-white leading-none">CARDIO-LUNG AI</h1>
              <p className="text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em] mt-1">Smart Diagnosis System</p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2 text-xs font-semibold px-4 py-2 bg-slate-900/50 rounded-full border border-slate-800"
          >
            <span className="status-dot pulsing bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
            <span className="text-slate-400">Backend Ready</span>
          </motion.div>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Controls */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="lg:col-span-5 space-y-8"
          >
            <motion.section variants={itemVariants} className="glass-panel p-8 rounded-[32px]">
              <div className="flex items-center space-x-3 mb-6">
                <Stethoscope size={20} className="text-blue-400" />
                <h2 className="text-lg font-bold text-white">Select Mode</h2>
              </div>

              <div className="grid grid-cols-2 gap-3 p-1 bg-slate-950/40 rounded-2xl border border-white/5">
                <button
                  onClick={() => setMode('heart')}
                  className={`flex items-center justify-center space-x-2 py-4 rounded-xl transition-all duration-300 ${mode === 'heart'
                    ? 'bg-blue-600 text-white shadow-xl shadow-blue-600/20'
                    : 'text-slate-500 hover:text-slate-300'
                    }`}
                >
                  <Heart size={18} />
                  <span className="text-sm font-bold">Cardiology</span>
                </button>
                <button
                  onClick={() => setMode('lung')}
                  className={`flex items-center justify-center space-x-2 py-4 rounded-xl transition-all duration-300 ${mode === 'lung'
                    ? 'bg-emerald-600 text-white shadow-xl shadow-emerald-600/20'
                    : 'text-slate-500 hover:text-slate-300'
                    }`}
                >
                  <Wind size={18} />
                  <span className="text-sm font-bold">Pulmonary</span>
                </button>
              </div>
            </motion.section>

            <motion.section variants={itemVariants} className="glass-panel p-8 rounded-[32px]">
              <div className="flex items-center space-x-3 mb-6">
                <FileAudio size={20} className="text-blue-400" />
                <h2 className="text-lg font-bold text-white">Upload Audio</h2>
              </div>

              <div
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                className={`relative group border-2 border-dashed rounded-3xl p-10 text-center transition-all duration-500 ${dragActive ? 'border-blue-400 bg-blue-400/5' :
                  file ? 'border-emerald-400/50 bg-emerald-400/5' : 'border-slate-800 hover:border-slate-700'
                  }`}
              >
                <input
                  type="file"
                  accept=".wav,.mp3"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="space-y-4">
                  <div className={`mx-auto w-16 h-16 rounded-2xl flex items-center justify-center transition-colors duration-500 ${file ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-900 text-slate-600'
                    }`}>
                    {file ? <CheckCircle2 size={32} /> : <Upload size={32} />}
                  </div>
                  <div>
                    <p className={`text-sm font-bold ${file ? 'text-emerald-300' : 'text-slate-300'}`}>
                      {file ? file.name : 'Click or drag audio file'}
                    </p>
                    <p className="text-[11px] text-slate-500 font-medium mt-1">WAV, MP3 up to 10MB</p>
                  </div>
                </div>
              </div>

              <button
                onClick={handlePredict}
                disabled={loading || !file}
                className={`w-full mt-8 py-5 rounded-2xl font-black tracking-wider shadow-2xl transition-all duration-500 flex items-center justify-center space-x-3 ${loading || !file
                  ? 'bg-slate-800 text-slate-600 cursor-not-allowed border border-white/5'
                  : 'bg-white text-slate-950 hover:bg-white/90 active:scale-95'
                  }`}
              >
                {loading ? <Loader2 className="animate-spin" /> : <Activity size={20} />}
                <span>{loading ? 'PROCESSING...' : 'ANALYZE AUDIO'}</span>
              </button>
            </motion.section>
          </motion.div>

          {/* Right Column: Results */}
          <div className="lg:col-span-7 h-full">
            <AnimatePresence mode="wait">
              {!result && !error && !loading ? (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="glass-panel h-full rounded-[40px] flex flex-col items-center justify-center p-12 text-center"
                >
                  <div className="w-24 h-24 bg-slate-900/50 rounded-[32px] flex items-center justify-center mb-8 border border-white/5">
                    <Waves className="text-blue-500/20" size={48} />
                  </div>
                  <h3 className="text-2xl font-black text-white mb-4 tracking-tight">Waiting for Input</h3>
                  <p className="text-slate-400 max-w-xs leading-relaxed">
                    Upload an auscultation recording to begin the AI-powered diagnostic process.
                  </p>
                </motion.div>
              ) : loading ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="glass-panel h-full rounded-[40px] flex flex-col items-center justify-center p-12"
                >
                  <div className="relative w-32 h-32 flex items-center justify-center mb-10">
                    <motion.div
                      animate={{ scale: [1, 1.4, 1], opacity: [0.3, 0.1, 0.3] }}
                      transition={{ duration: 2, repeat: Infinity }}
                      className="absolute inset-0 rounded-full bg-blue-500"
                    />
                    <motion.div
                      animate={{ scale: [1, 1.2, 1], opacity: [0.6, 0.2, 0.6] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                      className="absolute inset-4 rounded-full bg-blue-400"
                    />
                    <Activity size={48} className="text-white relative z-10" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2 pulsing">AI Analyzing...</h3>
                  <p className="text-blue-400 text-xs font-black tracking-widest uppercase">Extracting Pattern Weights</p>
                </motion.div>
              ) : error ? (
                <motion.div
                  key="error"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="glass-panel h-full rounded-[40px] flex flex-col items-center justify-center p-12 text-center border-red-500/20"
                >
                  <div className="w-20 h-20 bg-red-500/10 rounded-[28px] flex items-center justify-center mb-6 text-red-500">
                    <AlertCircle size={40} />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-4">Diagnostic Error</h3>
                  <div className="p-5 bg-red-400/5 rounded-2xl border border-red-500/10 text-red-300 text-sm font-medium leading-relaxed max-w-sm">
                    {error}
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="glass-panel h-full rounded-[40px] p-10 flex flex-col"
                >
                  <div className="flex items-center justify-between mb-10">
                    <div className="flex items-center space-x-3">
                      <BarChart3 size={20} className="text-emerald-400" />
                      <h2 className="text-lg font-bold text-white tracking-tight">Analysis Report</h2>
                    </div>
                    <div className="px-3 py-1 bg-emerald-500/10 rounded-full text-[10px] font-black tracking-wider text-emerald-400 border border-emerald-500/20 uppercase">
                      Confident
                    </div>
                  </div>

                  <div className="flex-1 space-y-10">
                    <div className="p-8 bg-gradient-to-br from-emerald-500/10 to-teal-500/5 rounded-[32px] border border-emerald-500/10">
                      <p className="text-[10px] font-black text-emerald-400 uppercase tracking-[0.2em] mb-3">Primary Diagnosis</p>
                      <h4 className="text-4xl font-black text-white tracking-tighter">
                        {mode === 'heart' ? result.predicted_disease : result.disease}
                      </h4>
                      <div className="mt-6">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-xs font-bold text-slate-400">Probability Score</span>
                          <span className="text-xs font-black text-emerald-400">{(result.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="h-2 w-full bg-slate-900 rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${result.confidence * 100}%` }}
                            transition={{ duration: 1, ease: "easeOut" }}
                            className="h-full bg-gradient-to-r from-emerald-500 to-teal-400"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 gap-4">
                      <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-4">Classification Details</p>
                      <div className="space-y-3">
                        {Object.entries(result.all_probabilities).map(([name, prob]) => (
                          <div key={name} className="flex items-center p-4 bg-white/5 rounded-2xl border border-white/5">
                            <span className="text-xs font-bold text-slate-300 w-24 truncate">{name}</span>
                            <div className="flex-1 h-1 bg-slate-900 rounded-full mx-4 overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${prob * 100}%` }}
                                className="h-full bg-blue-500/40"
                              />
                            </div>
                            <span className="text-[10px] font-black text-slate-500 w-8 text-right">{(prob * 100).toFixed(0)}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="mt-8 pt-8 border-t border-white/5 flex justify-between items-center text-[10px] font-bold text-slate-500 uppercase">
                    <span>Scan ID: #AI-{Math.floor(Math.random() * 90000) + 10000}</span>
                    <button className="hover:text-white transition-colors">Download Certificate</button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </main>

        <footer className="mt-20 border-t border-white/5 pt-8 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0 text-[11px] font-medium text-slate-600">
          <p>© 2026 CARDIO-PULMONARY DISEASE DETECTION SYSTEM</p>
          <div className="flex space-x-6 uppercase tracking-widest font-bold">
            <a href="#" className="hover:text-blue-400 transition-colors">Privacy</a>
            <a href="#" className="hover:text-blue-400 transition-colors">Security</a>
            <a href="#" className="hover:text-blue-400 transition-colors">API Docs</a>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
