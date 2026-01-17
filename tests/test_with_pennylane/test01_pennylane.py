import pennylane as qml
import numpy as np
import sys
import os
# Ensure we can import hilbertlens from the parent directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
sys.path.insert(0, PROJECT_ROOT)

import hilbertlens as hl

def main():
    print("=== HilbertLens with PennyLane ===")

    # 1. Define the Device
    n_qubits = 2
    dev = qml.device("default.qubit", wires=n_qubits)

    # 2. Define the Circuit (QNode)
    # The function must take the input data 'x' as its first argument
    # and return qml.state().
    @qml.qnode(dev)
    def circuit(x):
        # Initialize superposition
        for i in range(n_qubits):
            qml.Hadamard(wires=i)
        
        # Data Encoding (Angle Encoding)
        # We assume x has at least 2 features
        qml.RX(x[0], wires=0)
        qml.RY(x[1], wires=1)
        
        # Entanglement (creates geometric complexity)
        qml.CNOT(wires=[0, 1])
        
        # Data Re-uploading (optional, increases capacity)
        qml.RX(x[0], wires=1)
        
        return qml.state()

    # 3. Initialize HilbertLens
    # Pass the QNode directly. Framework can be 'auto' or 'pennylane'.
    # Note: 'params' argument is not required for PennyLane.
    lens = hl.QuantumLens(circuit, framework='pennylane')

    # MANUALLY SET THE PARAMETER COUNT
    # This tells the adapter "expect 2 features" so spectrum() knows what to do.
    # lens.adapter.n_params = 2

    # 4. Run the Full Diagnosis (Spectrum + Geometry)
    # This will automatically run spectrum() and geometry() checks.
    lens.diagnose()

    # --- Manual Checks (Optional) ---
    # Check 1: Geometry Preservation
    # Automatically generates a Swiss Roll dataset to test topology preservation
    print("\n--- Running Manual Geometry Check ---")
    lens.geometry(save_path="pennylane_geometry.png")
    
        
    # Check 2: Frequency Spectrum (Capacity)
    # mode='global' sweeps all inputs simultaneously to check total bandwidth
    print("\n--- Running Manual Spectrum Check ---")
    lens.spectrum(mode='global', save_path="pennylane_spectrum.png")



if __name__ == "__main__":
    main()