import { useState } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';
import { CloudRain, Sprout, MapPin, Cpu } from 'lucide-react';

export default function Predict() {
  const [formData, setFormData] = useState({
    farm_id: 'dummy_farm',
    field_id: 'dummy_field',
    crop: 'Wheat',
    cultivated_area: 10,
    soil_type: 'Loam',
    soil_ph: 6.5,
    soil_moisture: 30,
    soil_nutrients: 50,
    temperature: 25,
    rainfall: 100,
    humidity: 60,
  });
  
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const navigate = useNavigate();

  const handleFetchWeather = async () => {
    try {
      const { data } = await api.get('/weather?latitude=40.71&longitude=-74.00');
      setFormData({ ...formData, temperature: data.temperature, humidity: data.humidity, rainfall: data.precipitation || formData.rainfall });
    } catch (e) {
      alert("Weather data unavailable. Using manual values.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setLoadingStep('Validating input...');
    
    setTimeout(() => setLoadingStep('Preprocessing features...'), 1000);
    setTimeout(() => setLoadingStep('Running classical models...'), 2000);
    setTimeout(() => setLoadingStep('Encoding quantum features...'), 3500);
    setTimeout(() => setLoadingStep('Computing quantum kernel matrix...'), 5000);
    
    try {
      const { data } = await api.post('/predictions', formData);
      setLoading(false);
      navigate(`/predictions/${data.id}`, { state: { result: data } });
    } catch (e) {
      alert("Prediction failed");
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center space-y-4">
        <Cpu className="w-16 h-16 text-emerald-500 animate-pulse" />
        <h2 className="text-2xl font-bold">{loadingStep}</h2>
        <p className="text-slate-500">Qiskit Aer - Local Simulator Executing</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold">New Crop Yield Prediction</h1>
        <p className="text-slate-500 mt-2">Analyze agricultural conditions using classical and quantum-enhanced machine learning.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <section className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2"><Sprout className="w-5 h-5 text-emerald-600" /> Farm & Crop Data</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Crop</label>
              <select className="w-full p-2 border rounded dark:bg-slate-800" value={formData.crop} onChange={e => setFormData({...formData, crop: e.target.value})}>
                <option>Wheat</option>
                <option>Corn</option>
                <option>Rice</option>
                <option>Soybean</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Cultivated Area (Hectares)</label>
              <input type="number" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.cultivated_area} onChange={e => setFormData({...formData, cultivated_area: +e.target.value})} />
            </div>
          </div>
        </section>

        <section className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2"><MapPin className="w-5 h-5 text-amber-600" /> Soil Data</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Soil Type</label>
              <select className="w-full p-2 border rounded dark:bg-slate-800" value={formData.soil_type} onChange={e => setFormData({...formData, soil_type: e.target.value})}>
                <option>Clay</option>
                <option>Sandy</option>
                <option>Loam</option>
                <option>Silt</option>
              </select>
            </div>
            <div><label className="block text-sm font-medium mb-1">Soil pH</label><input type="number" step="0.1" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.soil_ph} onChange={e => setFormData({...formData, soil_ph: +e.target.value})} /></div>
            <div><label className="block text-sm font-medium mb-1">Moisture (%)</label><input type="number" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.soil_moisture} onChange={e => setFormData({...formData, soil_moisture: +e.target.value})} /></div>
            <div><label className="block text-sm font-medium mb-1">Nutrients Level</label><input type="number" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.soil_nutrients} onChange={e => setFormData({...formData, soil_nutrients: +e.target.value})} /></div>
          </div>
        </section>

        <section className="bg-white dark:bg-slate-900 p-6 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold flex items-center gap-2"><CloudRain className="w-5 h-5 text-blue-500" /> Weather Data</h2>
            <button type="button" onClick={handleFetchWeather} className="text-sm bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-3 py-1 rounded hover:bg-blue-100 transition-colors">Fetch Live Weather</button>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div><label className="block text-sm font-medium mb-1">Temperature (°C)</label><input type="number" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.temperature} onChange={e => setFormData({...formData, temperature: +e.target.value})} /></div>
            <div><label className="block text-sm font-medium mb-1">Rainfall (mm)</label><input type="number" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.rainfall} onChange={e => setFormData({...formData, rainfall: +e.target.value})} /></div>
            <div><label className="block text-sm font-medium mb-1">Humidity (%)</label><input type="number" className="w-full p-2 border rounded dark:bg-slate-800" value={formData.humidity} onChange={e => setFormData({...formData, humidity: +e.target.value})} /></div>
          </div>
        </section>
        
        <button type="submit" className="w-full bg-emerald-600 text-white p-4 rounded-xl font-bold text-lg hover:bg-emerald-700 shadow-lg flex justify-center items-center gap-2">
          <Cpu className="w-5 h-5" /> Execute Quantum & Classical Pipeline
        </button>
      </form>
    </div>
  );
}
