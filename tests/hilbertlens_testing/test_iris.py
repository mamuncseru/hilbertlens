
import numpy as np
from sklearn.datasets import load_iris
from qiskit.circuit.library import zz_feature_map, pauli_feature_map

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

print(f"Adding PROJECT_ROOT to sys.path: {PROJECT_ROOT}")

sys.path.insert(0, PROJECT_ROOT)
import hilbertlens as hl

def test_iris_diagnosis():
    print("=== Testing Scalability: Iris Dataset (4 Features) ===")
    
    # 1. Load Data (4 Features)
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    # Select only the first two classes (0 and 1) for cleaner binary visualization
    # (Though HilbertLens works with multi-class, binary is easier to check visually)
    mask = y < 2
    X = X[mask]
    y = y[mask]
    
    # Normalize Data: Scale to [0, pi] to avoid aliasing (wrapping around Bloch sphere)
    # Using 'pi' instead of '2pi' often gives better geometry scores
    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    X_norm = (np.pi/2) * (X - X_min) / (X_max - X_min)
    
    print(f"Data Shape: {X_norm.shape} (N={X_norm.shape[0]}, Features={X_norm.shape[1]})")

    # 2. Create Matching Circuit
    # We use Qiskit's built-in ZZFeatureMap which automatically builds
    # a circuit with 'feature_dimension' parameters.
    # Reps=2 gives it more depth (capacity).
    print("Creating 4-Qubit ZZFeatureMap...")
    # qc = zz_feature_map(feature_dimension=4, reps=1, entanglement='linear')
    qc = pauli_feature_map(feature_dimension=4, reps=1, paulis=['Z'])
    
    # Extract the parameters object from the library circuit
    # ZZFeatureMap stores them in .parameters
    params = list(qc.parameters)
    
    # 3. Initialize Lens
    # The new adapter will automatically detect: 4 data columns -> 4 circuit params
    lens = hl.QuantumLens(qc, params=params, framework='qiskit')

    # 4. Run Geometry Check
    # This proves the adapter can map 4D input -> 4D parameters without crashing
    print("\n--- Running Geometry Check ---")
    lens.geometry(X_data=X_norm, save_path="iris_geometry.png")

    # 5. Run Spectrum Check
    # Global sweep will vary all 4 inputs simultaneously
    print("\n--- Running Spectrum Check ---")
    lens.spectrum(mode='global', save_path="iris_spectrum.png")

    # 6. Call The Doctor
    lens.diagnose()

if __name__ == "__main__":
    test_iris_diagnosis()