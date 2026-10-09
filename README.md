# QuantumYield AI - Quantum AI-Based Crop Yield Prediction System

## 1. Project Overview
This project is an implementation of a Quantum AI-based Crop Yield Prediction System using weather, soil, and farming data (Problem Statement ID 29). It utilizes a modern tech stack to provide a complete web application that demonstrates classical and quantum-enhanced machine learning techniques.

## 2. Architecture
- **Frontend**: React, Vite, Tailwind CSS 4, React Router, Recharts, Lucide-React
- **Backend**: FastAPI, Pydantic, Uvicorn
- **Database**: MongoDB (via mongomock for easy zero-setup execution)
- **Machine Learning**: Scikit-learn, Pandas, Numpy, Joblib
- **Quantum Computing**: Qiskit, Qiskit Aer, Qiskit Machine Learning

## 3. Dataset
The project uses a synthetic dataset replicating the statistical properties of the **CC0 CYCLeSS** dataset. It maps `temperature`, `rainfall`, `humidity`, `soil_ph`, `soil_moisture`, `soil_nutrients`, and `soil_type` to a crop `yield`.

## 4. Machine Learning Methodology
- **Classical Models**: 
  - Histogram Gradient Boosting Regressor (primary model for speed and accuracy).
  - Random Forest Regressor (comparison model).
- **Quantum Algorithm**: 
  - SVR (Support Vector Regression) with a **Fidelity Quantum Kernel**.
  - The quantum kernel evaluates the similarity of feature vectors encoded using `ZZFeatureMap` executed on `Qiskit Aer` (local simulator).

## 5. Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.9+)

### Installation & Execution

#### 1. Start the Backend
```bash
cd backend
python -m venv venv
# Activate the environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt (or simply install fastapi, uvicorn, qiskit, scikit-learn etc.)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*(Note: If mongomock is installed, no external MongoDB instance is needed. It runs in memory).*

#### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

### Future Scope
- Integration with real Quantum Hardware (e.g. IBM Quantum Experience) when queue times are acceptable.
- Dynamic data streaming from live IoT agricultural sensors.
