import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

print(f"Adding PROJECT_ROOT to sys.path: {PROJECT_ROOT}")

sys.path.insert(0, PROJECT_ROOT)
import hilbertlens as hl


def test_two_moons():
    print("=== Testing with Real Data: Two Moons ===")
    
    # 1. Generate Data (2D)
    # 2 features, 200 samples
    X, y = make_moons(n_samples=200, noise=0.1, random_state=42)
    
    # Normalize data to range [0, 2pi] for quantum encoding
    # Min-Max scaling to [-pi, pi] or similar usually works best
    # X = 2 * np.pi * (X - X.min(0)) / (X.max(0) - X.min(0))
    # NEW: Half rotation (Safer, preserves local neighborhoods)
    X = np.pi * (X - X.min(0)) / (X.max(0) - X.min(0))
    
    print(f"Data Shape: {X.shape} (2 Features)")

    # 2. Create a Matching 2-Qubit Circuit
    # We use a standard "ZZFeatureMap" style ansatz
    # Structure: H -> Rz(x) -> CNOT -> Rz(x)
    n_features = 2
    x = ParameterVector('x', n_features)
    qc = QuantumCircuit(n_features)
    
    # Layer 1: Encode individual features
    for i in range(n_features):
        qc.h(i)
        qc.rz(x[i], i)
        
    # Layer 2: Entanglement (Interaction)
    qc.cx(0, 1)
    
    # Layer 3: Encode again (Optional, helps expressibility)
    qc.rz(x[1], 0) 
    qc.rz(x[0], 1)
    
    print("Circuit Created: 2-Qubit Entangled Network.")

    # 3. Initialize Lens
    lens = hl.QuantumLens(qc, params=list(x), framework='qiskit')

    # 4. Run Geometry Check with EXPLICIT Data
    # We pass 'X' so it doesn't auto-generate the Swiss Roll
    print("\n--- Running Geometry Check (Two Moons) ---")
    lens.geometry(X_data=X, save_path="moons_geometry.png")

    # 5. Run Spectrum (Global Sweep)
    # We want to see if the circuit interacts well
    print("\n--- Running Spectrum Check ---")
    lens.spectrum(mode='global', save_path="moons_spectrum.png")

    # 6. Call the Doctor
    # Since we already ran the tests, it won't say "Data missing"
    lens.diagnose()

if __name__ == "__main__":
    test_two_moons()