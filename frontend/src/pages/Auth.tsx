import { useState, useContext } from 'react';
import { AuthContext } from '../App';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        const { data } = await api.post('/auth/login', formData);
        localStorage.setItem('token', data.access_token);
      } else {
        await api.post('/auth/signup', { name, email, password });
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        const { data } = await api.post('/auth/login', formData);
        localStorage.setItem('token', data.access_token);
      }
      const { data: user } = await api.get('/auth/me');
      setUser(user);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed');
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-slate-100 dark:bg-slate-900">
      <div className="w-full max-w-md p-8 bg-white dark:bg-slate-800 rounded-xl shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6 text-emerald-800 dark:text-emerald-400">QuantumYield AI</h1>
        <h2 className="text-xl font-semibold text-center mb-4">{isLogin ? 'Login' : 'Sign Up'}</h2>
        {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <input className="w-full p-2 border rounded dark:bg-slate-700" placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
          )}
          <input className="w-full p-2 border rounded dark:bg-slate-700" placeholder="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          <input className="w-full p-2 border rounded dark:bg-slate-700" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          <button type="submit" className="w-full bg-emerald-600 text-white p-2 rounded hover:bg-emerald-700">{isLogin ? 'Login' : 'Sign Up'}</button>
        </form>
        <p className="mt-4 text-center text-sm cursor-pointer hover:underline" onClick={() => setIsLogin(!isLogin)}>
          {isLogin ? "Don't have an account? Sign up" : "Already have an account? Login"}
        </p>
      </div>
    </div>
  );
}
