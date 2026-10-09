
import { Link } from 'react-router-dom';
import { Cpu, CloudRain, Binary, Sprout, Network } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-slate-950 text-white font-sans overflow-x-hidden">
      {/* Hero Section */}
      <div className="relative pt-32 pb-20 px-8 max-w-7xl mx-auto flex flex-col items-center text-center">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-emerald-600/20 blur-[120px] rounded-full -z-10" />
        <h1 className="text-6xl font-extrabold tracking-tight mb-6">QuantumYield AI</h1>
        <p className="text-2xl text-emerald-400 mb-4">Quantum AI-Based Crop Yield Prediction</p>
        <p className="text-xl text-slate-400 mb-10 max-w-2xl">Predict Better. Farm Smarter. Grow More.</p>
        
        <div className="flex gap-4">
          <Link to="/auth" className="px-8 py-4 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-lg font-bold transition-all shadow-[0_0_20px_rgba(16,185,129,0.4)]">Start Predicting</Link>
          <Link to="/about" className="px-8 py-4 bg-slate-800 hover:bg-slate-700 rounded-lg text-lg font-bold transition-all">Explore the Technology</Link>
        </div>
      </div>

      {/* Pipeline Section */}
      <div className="py-24 bg-slate-900 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-8">
          <h2 className="text-3xl font-bold text-center mb-16">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
            {/* 01 */}
            <div className="flex flex-col items-center text-center z-10">
              <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4 border border-slate-700 text-blue-400"><CloudRain /></div>
              <h3 className="font-bold mb-2">01. Agricultural Data</h3>
              <p className="text-sm text-slate-400">Weather + Soil + Farming Data</p>
            </div>
            {/* 02 */}
            <div className="flex flex-col items-center text-center z-10">
              <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4 border border-slate-700 text-amber-400"><Sprout /></div>
              <h3 className="font-bold mb-2">02. Data Processing</h3>
              <p className="text-sm text-slate-400">Cleaning + Scaling + Features</p>
            </div>
            {/* 03 */}
            <div className="flex flex-col items-center text-center z-10">
              <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4 border border-slate-700 text-purple-400"><Network /></div>
              <h3 className="font-bold mb-2">03. AI Models</h3>
              <p className="text-sm text-slate-400">Classical ML + Quantum Kernel</p>
            </div>
            {/* 04 */}
            <div className="flex flex-col items-center text-center z-10">
              <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4 border border-slate-700 text-emerald-400"><Binary /></div>
              <h3 className="font-bold mb-2">04. Prediction</h3>
              <p className="text-sm text-slate-400">Crop Yield Estimation</p>
            </div>
            {/* 05 */}
            <div className="flex flex-col items-center text-center z-10">
              <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4 border border-slate-700 text-teal-400"><Cpu /></div>
              <h3 className="font-bold mb-2">05. Analysis</h3>
              <p className="text-sm text-slate-400">Metrics + Comparison + Insights</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
