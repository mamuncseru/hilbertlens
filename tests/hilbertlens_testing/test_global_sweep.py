import sys
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

print(f"Adding PROJECT_ROOT to sys.path: {PROJECT_ROOT}")

sys.path.insert(0, PROJECT_ROOT)

import hilbertlens as hl

def test_adder_circuit():
    print("=== Testing Frequency Addition (Local vs Global) ===")
    
    # 1. Create a "Frequency Adder" Circuit
    # Logic: Apply rotation x[0], then rotation x[1] on the SAME wire.
    # Effect: Rotation by angle (x[0] + x[1])
    x = ParameterVector('x', 2)
    qc = QuantumCircuit(1)
    
    qc.rx(x[0], 0)
    qc.rx(x[1], 0)
    
    print("Circuit: Rx(x0) -> Rx(x1)")

    lens = hl.QuantumLens(qc, params=list(x), framework='qiskit')

    # Test 1: Local Sweep (Feature 0)
    # x[0] = t, x[1] = 0.  Total Angle = t.
    # Expected Freq: 0.5 (standard rotation)
    print("\n--- Running Local Sweep (Feature 0) ---")
    stats_local = lens.spectrum(mode='local', feature_index=0, save_path="spectrum_adder_local.png")
    print(f"Local Peak: k={stats_local['dominant_freq']:.1f}")

    # Test 2: Global Sweep
    # x[0] = t, x[1] = t.  Total Angle = 2t.
    # Expected Freq: 1.0 (double rotation)
    print("\n--- Running Global Sweep (All Features) ---")
    stats_global = lens.spectrum(mode='global', save_path="spectrum_adder_global.png")
    print(f"Global Peak: k={stats_global['dominant_freq']:.1f}")
    
    # Assertion
    if stats_global['dominant_freq'] > stats_local['dominant_freq']:
        print("\nSUCCESS: Global sweep detected higher frequency (Addition worked).")
    else:
        print("\nFAILURE: Frequencies look the same. Check adapter logic.")

if __name__ == "__main__":
    test_adder_circuit()