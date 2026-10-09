import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Qiskit imports
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_aer import Aer
from sklearn.svm import SVR

def train_classical_models(data_path="dataset.csv", models_dir="../models"):
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    df = pd.read_csv(data_path)
    X = df.drop('yield', axis=1)
    y = df['yield']
    
    # Preprocessing
    num_features = ['temperature', 'rainfall', 'humidity', 'soil_ph', 'soil_moisture', 'soil_nutrients']
    cat_features = ['soil_type', 'crop']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_features)
        ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. HistGradientBoostingRegressor
    hgb = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', HistGradientBoostingRegressor(random_state=42))
    ])
    
    hgb.fit(X_train, y_train)
    y_pred = hgb.predict(X_test)
    
    metrics = {
        'mae': mean_absolute_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'r2': r2_score(y_test, y_pred)
    }
    
    print("Histogram Gradient Boosting Metrics:", metrics)
    joblib.dump(hgb, os.path.join(models_dir, 'hgb_model.joblib'))
    joblib.dump(metrics, os.path.join(models_dir, 'hgb_metrics.joblib'))
    
    # 2. Random Forest for comparison
    from sklearn.ensemble import RandomForestRegressor
    rf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_metrics = {
        'mae': mean_absolute_error(y_test, rf_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, rf_pred)),
        'r2': r2_score(y_test, rf_pred)
    }
    print("Random Forest Metrics:", rf_metrics)
    joblib.dump(rf, os.path.join(models_dir, 'rf_model.joblib'))
    joblib.dump(rf_metrics, os.path.join(models_dir, 'rf_metrics.joblib'))
    
    # 3. Quantum Kernel Regression (using SVR)
    # Since quantum simulation is slow, we use a tiny subset of data to train the SVR and save it.
    print("Training Quantum Kernel Model on subset...")
    subset_size = 100
    X_train_q = X_train.iloc[:subset_size]
    y_train_q = y_train.iloc[:subset_size]
    X_test_q = X_test.iloc[:20]
    y_test_q = y_test.iloc[:20]
    
    # For quantum, we usually reduce feature dimension. Let's PCA to 4 features.
    from sklearn.decomposition import PCA
    q_preprocessor = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('pca', PCA(n_components=4))
    ])
    
    X_train_q_scaled = q_preprocessor.fit_transform(X_train_q)
    X_test_q_scaled = q_preprocessor.transform(X_test_q)
    
    feature_map = ZZFeatureMap(feature_dimension=4, reps=2, entanglement='linear')
    # Use FidelityQuantumKernel without setting 'backend' explicitly since it will use local statevector by default in new qiskit
    qkernel = FidelityQuantumKernel(feature_map=feature_map)
    
    # Compute training kernel matrix
    matrix_train = qkernel.evaluate(x_vec=X_train_q_scaled)
    matrix_test = qkernel.evaluate(x_vec=X_test_q_scaled, y_vec=X_train_q_scaled)
    
    qsvr = SVR(kernel='precomputed')
    qsvr.fit(matrix_train, y_train_q)
    
    y_pred_q = qsvr.predict(matrix_test)
    q_metrics = {
        'mae': mean_absolute_error(y_test_q, y_pred_q),
        'rmse': np.sqrt(mean_squared_error(y_test_q, y_pred_q)),
        'r2': r2_score(y_test_q, y_pred_q)
    }
    print("Quantum Kernel Metrics:", q_metrics)
    
    # Save components
    joblib.dump(q_preprocessor, os.path.join(models_dir, 'q_preprocessor.joblib'))
    joblib.dump(qsvr, os.path.join(models_dir, 'qsvr_model.joblib'))
    joblib.dump(X_train_q_scaled, os.path.join(models_dir, 'X_train_q_scaled.joblib'))
    joblib.dump(q_metrics, os.path.join(models_dir, 'q_metrics.joblib'))

if __name__ == "__main__":
    import os
    if not os.path.exists("dataset.csv"):
        from generate_data import generate_cycless_dataset
        generate_cycless_dataset(2000, "dataset.csv")
    train_classical_models()
