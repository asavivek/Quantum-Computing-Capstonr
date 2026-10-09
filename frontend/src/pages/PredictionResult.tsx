
import { useLocation, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, Beaker } from 'lucide-react';

export default function PredictionResult() {
  const { state } = useLocation();
  const result = state?.result;

  if (!result) return <div>No prediction data found.</div>;

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <Link to="/dashboard" className="flex items-center text-slate-500 hover:text-slate-800 dark:hover:text-slate-200">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Dashboard
      </Link>
      
      <div className="bg-gradient-to-r from-emerald-700 to-teal-800 p-8 rounded-2xl text-white shadow-xl flex flex-col md:flex-row justify-between items-center">
        <div>
          <h2 className="text-emerald-100 font-medium text-lg uppercase tracking-wider mb-2">Predicted Yield</h2>
          <div className="text-6xl font-bold">{result.predicted_yield.toFixed(2)} <span className="text-2xl font-normal">tons/ha</span></div>
          <p className="mt-4 opacity-80 flex items-center gap-2"><CheckCircle className="w-5 h-5"/> Based on {result.selected_model}</p>
        </div>
        <div className="mt-6 md:mt-0 text-right">
          <p className="text-xl font-semibold">{result.input_features.crop}</p>
          <p className="opacity-80">Farm ID: {result.farm_id}</p>
          <p className="opacity-80">Date: {new Date(result.created_at).toLocaleDateString()}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
          <h3 className="text-xl font-bold mb-4">Model Comparison</h3>
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800">
                <th className="py-2">Model</th>
                <th>Prediction</th>
                <th>RMSE</th>
                <th>R²</th>
              </tr>
            </thead>
            <tbody>
              {result.model_results.map((m: any, i: number) => (
                <tr key={i} className="border-b border-slate-100 dark:border-slate-800/50">
                  <td className="py-3 font-medium">{m.model}</td>
                  <td>{m.prediction.toFixed(2)}</td>
                  <td>{m.metrics.rmse.toFixed(3)}</td>
                  <td>{m.metrics.r2.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-slate-900 text-white p-6 rounded-xl shadow-sm border border-slate-800">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2 text-teal-400"><Beaker className="w-5 h-5"/> Quantum Metadata</h3>
          <div className="space-y-4">
            {Object.entries(result.quantum_metadata).map(([k, v]) => (
              <div key={k}>
                <p className="text-slate-400 text-sm uppercase">{k.replace('_', ' ')}</p>
                <p className="font-mono">{v as string}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
