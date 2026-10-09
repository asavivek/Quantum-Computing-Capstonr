import { useEffect, useState } from 'react';
import api from '../services/api';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [predictions, setPredictions] = useState<any[]>([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const { data } = await api.get('/predictions');
        setPredictions(data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchStats();
  }, []);

  const chartData = predictions.slice(0, 5).map(p => ({
    name: new Date(p.created_at).toLocaleDateString(),
    Classical: p.model_results[0].prediction,
    Quantum: p.model_results[2].prediction,
  }));

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
          <h3 className="text-slate-500 text-sm font-medium">Total Predictions</h3>
          <p className="text-3xl font-bold mt-2">{predictions.length}</p>
        </div>
        <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
          <h3 className="text-slate-500 text-sm font-medium">Quantum Models Executed</h3>
          <p className="text-3xl font-bold mt-2">{predictions.length}</p>
        </div>
        <div className="bg-emerald-600 p-6 rounded-xl shadow-sm text-white flex flex-col justify-center items-start">
          <h3 className="text-emerald-100 text-sm font-medium">Ready to Analyze?</h3>
          <Link to="/predict" className="mt-2 bg-white text-emerald-700 px-4 py-2 rounded-lg font-medium hover:bg-emerald-50 transition-colors">
            New Prediction
          </Link>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
        <h2 className="text-xl font-bold mb-6">Recent Prediction Comparisons</h2>
        {predictions.length > 0 ? (
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="Classical" fill="#0f172a" />
                <Bar dataKey="Quantum" fill="#14b8a6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="h-40 flex items-center justify-center text-slate-500">
            No predictions yet. Run your first crop-yield analysis.
          </div>
        )}
      </div>
    </div>
  );
}
