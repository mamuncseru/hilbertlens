import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

print(f"Adding PROJECT_ROOT to sys.path: {PROJECT_ROOT}")

sys.path.insert(0, PROJECT_ROOT)

import hilbertlens as hl

def test_full_library():
    print("=== Testing Full HilbertLens Library ===")
    
    # 1. Define a Multi-Dimensional Circuit (ZZFeatureMap style)
    # We need 3 inputs for the Swiss Roll (X, Y, Z coordinates)
    n_features = 3
    x = ParameterVector('x', n_features)
    
    qc = QuantumCircuit(n_features)
    
    # Simple Angle Encoding: H -> Rz(x)
    for i in range(n_features):
        qc.h(i)
        qc.rz(x[i], i)
    
    # Add some entanglement so the geometry isn't trivial
    qc.cx(0, 1)
    qc.cx(1, 2)
    
    print("Circuit created (3 qubits, 3 features).")

    # 2. Initialize the Lens
    # Note: We pass the ParameterVector 'x' so the adapter knows where to put data
    lens = hl.QuantumLens(qc, params=list(x), framework='qiskit')

    # 3. Run Spectrum Check (Will use 1D sweep on first parameter by default)
    print("\n--- Running Spectrum Check ---")
    lens.spectrum(save_path="final_spectrum.png")

    # 4. Run Geometry Check (Will generate Swiss Roll automatically)
    print("\n--- Running Geometry Check ---")
    lens.geometry(save_path="final_geometry.png")

if __name__ == "__main__":
    test_full_library()