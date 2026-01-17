import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
import pennylane as qml

# Ensure we can import hilbertlens from the parent directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
sys.path.insert(0, PROJECT_ROOT)

import hilbertlens as hl

def test_two_moons_pennylane():
    print("=== Testing with Real Data: Two Moons (PennyLane) ===")
    
    # 1. Generate Data (Same as Qiskit version)
    X, y = make_moons(n_samples=200, noise=0.1, random_state=42)
    
    # Normalize data [0, pi]
    X = np.pi * (X - X.min(0)) / (X.max(0) - X.min(0))
    print(f"Data Shape: {X.shape} (2 Features)")

    # 2. Define the PennyLane Circuit
    # Replicates the structure: H -> Rz(x) -> CNOT -> Rz(swapped x)
    n_qubits = 2
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit(x):
        # Layer 1: Encode individual features (H -> Rz)
        # qc.h(0); qc.rz(x[0], 0)
        qml.Hadamard(wires=0)
        qml.RZ(x[0], wires=0)
        
        # qc.h(1); qc.rz(x[1], 1)
        qml.Hadamard(wires=1)
        qml.RZ(x[1], wires=1)
        
        # Layer 2: Entanglement
        # qc.cx(0, 1)
        qml.CNOT(wires=[0, 1])
        
        # Layer 3: Encode again (swapped features)
        # qc.rz(x[1], 0)
        qml.RZ(x[1], wires=0)
        
        # qc.rz(x[0], 1)
        qml.RZ(x[0], wires=1)
        
        # Must return state for HilbertLens analysis
        return qml.state()

    print("Circuit Created: PennyLane QNode (2 Qubits).")
    
    # Optional: Draw the circuit
    try:
        # Draw with dummy data to visualize structure
        print("\nCircuit Diagram:")
        print(qml.draw(circuit)([0.1, 0.2]))
    except Exception as e:
        print(f"Could not draw circuit: {e}")

    # 3. Initialize Lens
    # No 'params' list needed for PennyLane
    lens = hl.QuantumLens(circuit, framework='pennylane')

    # 4. Run Geometry Check
    # Important: Running this first with 'X_data' allows the adapter 
    # to learn that n_params=2 automatically.
    print("\n--- Running Geometry Check (Two Moons) ---")
    lens.geometry(X_data=X, save_path="moons_geometry_pl.png")

    # 5. Run Spectrum Check
    print("\n--- Running Spectrum Check ---")
    lens.spectrum(mode='global', save_path="moons_spectrum_pl.png")

    # 6. Call the Doctor
    lens.diagnose()

if __name__ == "__main__":
    test_two_moons_pennylane()