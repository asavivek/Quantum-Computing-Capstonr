
import { Cpu, Network, Binary } from 'lucide-react';

export default function QuantumInsights() {
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">Quantum Insights</h1>
      <div className="bg-white dark:bg-slate-900 p-8 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 space-y-6">
        
        <div className="flex gap-4 items-start">
          <div className="p-3 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg"><Cpu className="w-6 h-6"/></div>
          <div>
            <h3 className="text-xl font-bold">Quantum Backend: Qiskit Aer — Local Simulator</h3>
            <p className="text-slate-600 dark:text-slate-400 mt-2">Because physical quantum hardware is not used during standard prediction workflows to avoid queue times, we utilize the high-performance Qiskit Aer local simulator. It computes the exact statevector representing the quantum state.</p>
          </div>
        </div>

        <div className="flex gap-4 items-start">
          <div className="p-3 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 rounded-lg"><Network className="w-6 h-6"/></div>
          <div>
            <h3 className="text-xl font-bold">Algorithm: Fidelity Quantum Kernel</h3>
            <p className="text-slate-600 dark:text-slate-400 mt-2">A quantum kernel measures similarity between encoded data points in a quantum feature space. These similarities are used by the kernel-based learning model (SVR). The project investigates whether quantum feature-space representations can provide useful learning characteristics for crop-yield prediction.</p>
          </div>
        </div>

        <div className="flex gap-4 items-start">
          <div className="p-3 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-lg"><Binary className="w-6 h-6"/></div>
          <div>
            <h3 className="text-xl font-bold">Complexity</h3>
            <p className="text-slate-600 dark:text-slate-400 mt-2">Kernel matrix construction requires approximately O(n²) pairwise evaluations for n samples. Space for the complete kernel matrix is O(n²).</p>
          </div>
        </div>

      </div>
    </div>
  );
}
