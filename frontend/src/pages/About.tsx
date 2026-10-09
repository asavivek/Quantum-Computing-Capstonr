

export default function About() {
  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <h1 className="text-3xl font-bold">About QuantumYield AI</h1>
      <div className="prose dark:prose-invert max-w-none">
        <h3>Problem Statement — ID 29</h3>
        <p className="text-lg bg-emerald-50 dark:bg-emerald-900/20 p-4 border-l-4 border-emerald-500 italic">"Design a Quantum AI-based Crop Yield Prediction System using weather, soil, and farming data."</p>
        
        <h3>Objective</h3>
        <p>Accurate crop-yield estimation from agricultural variables can support data-driven agricultural analysis.</p>

        <h3>Machine Learning & Quantum Computing</h3>
        <ul>
          <li><strong>Classical Approach:</strong> Histogram Gradient Boosting and Random Forest regression models.</li>
          <li><strong>Quantum Approach:</strong> Fidelity Quantum Kernel using Qiskit Aer.</li>
        </ul>

        <h3>Dataset</h3>
        <p>Uses a simulated equivalent of the CC0 CYCLeSS agricultural dataset, generating synthetic correlations for validation.</p>
        
        <h3>Technology</h3>
        <p>React + FastAPI + MongoDB (mocked) + Python + Scikit-learn + Qiskit Aer.</p>

        <h3>Limitations</h3>
        <p>The quantum component is evaluated using a local simulator rather than physical quantum hardware. This is technically honest and ensures stable and fast evaluation for demonstration purposes without requiring API tokens for IBM Quantum systems.</p>
      </div>
    </div>
  );
}
