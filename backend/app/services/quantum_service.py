import os
import joblib
import pandas as pd
import numpy as np

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'models')

# Global cache for models
_models_cache = {}

def load_models():
    if _models_cache:
        return _models_cache
    
    try:
        _models_cache['hgb_model'] = joblib.load(os.path.join(MODELS_DIR, 'hgb_model.joblib'))
        _models_cache['hgb_metrics'] = joblib.load(os.path.join(MODELS_DIR, 'hgb_metrics.joblib'))
        
        _models_cache['rf_model'] = joblib.load(os.path.join(MODELS_DIR, 'rf_model.joblib'))
        _models_cache['rf_metrics'] = joblib.load(os.path.join(MODELS_DIR, 'rf_metrics.joblib'))
        
        _models_cache['q_preprocessor'] = joblib.load(os.path.join(MODELS_DIR, 'q_preprocessor.joblib'))
        _models_cache['qsvr_model'] = joblib.load(os.path.join(MODELS_DIR, 'qsvr_model.joblib'))
        _models_cache['X_train_q_scaled'] = joblib.load(os.path.join(MODELS_DIR, 'X_train_q_scaled.joblib'))
        _models_cache['q_metrics'] = joblib.load(os.path.join(MODELS_DIR, 'q_metrics.joblib'))
    except Exception as e:
        print(f"Failed to load models: {e}. Models might not be trained yet.")
        
    return _models_cache

def run_prediction(input_data: dict):
    models = load_models()
    if not models:
        raise ValueError("Models not trained yet.")
        
    # Convert input to DataFrame
    df = pd.DataFrame([input_data])
    
    # Predict Classical
    hgb = models['hgb_model']
    hgb_pred = float(hgb.predict(df)[0])
    
    rf = models['rf_model']
    rf_pred = float(rf.predict(df)[0])
    
    # Predict Quantum
    q_prep = models['q_preprocessor']
    X_q_scaled = q_prep.transform(df)
    
    from qiskit.circuit.library import ZZFeatureMap
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    
    feature_map = ZZFeatureMap(feature_dimension=4, reps=2, entanglement='linear')
    qkernel = FidelityQuantumKernel(feature_map=feature_map)
    
    # Compute test kernel matrix against training support vectors
    matrix_test = qkernel.evaluate(x_vec=X_q_scaled, y_vec=models['X_train_q_scaled'])
    
    qsvr = models['qsvr_model']
    qsvr_pred = float(qsvr.predict(matrix_test)[0])
    
    # Format results
    results = [
        {"model": "Histogram Gradient Boosting", "prediction": hgb_pred, "metrics": models['hgb_metrics']},
        {"model": "Random Forest", "prediction": rf_pred, "metrics": models['rf_metrics']},
        {"model": "Quantum Kernel Model", "prediction": qsvr_pred, "metrics": models['q_metrics']}
    ]
    
    q_meta = {
        "backend": "Qiskit Aer - Local Simulator",
        "algorithm": "Fidelity Quantum Kernel",
        "qubits": 4,
        "encoded_features": 4,
        "kernel_type": "State Fidelity",
        "complexity_note": "Kernel matrix construction is approximately O(n^2) pairwise evaluations."
    }
    
    return {
        "results": results,
        "selected_model": "Histogram Gradient Boosting",
        "predicted_yield": hgb_pred,
        "metrics": models['hgb_metrics'],
        "quantum_metadata": q_meta
    }
