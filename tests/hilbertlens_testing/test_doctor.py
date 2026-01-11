
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

def test_the_doctor():
    print("=== Testing HilbertLens Diagnosis Module ===")
    
    # 1. Create a "Deep" Circuit (High Capacity)
    # We use Data Re-uploading to simulate a "Smart" circuit
    # L1: Rx(x) -> L2: Rx(x) -> L3: Rx(x)
    # Expected Freq: k=3.0 (Rich)
    x = ParameterVector('x', 1)
    qc = QuantumCircuit(1)
    
    # Layer 1
    qc.rx(x[0], 0)
    qc.barrier()
    # Layer 2
    qc.rx(x[0], 0)
    qc.barrier()
    # Layer 3
    qc.rx(x[0], 0)
    
    print("Circuit Created: Depth=3 Data Re-uploading.")

    # 2. Initialize
    lens = hl.QuantumLens(qc, params=list(x), framework='qiskit')

    # 3. Call The Doctor directly
    # Note: We haven't run spectrum() or geometry() manually.
    # The doctor should Auto-Run them.
    lens.diagnose()

if __name__ == "__main__":
    test_the_doctor()