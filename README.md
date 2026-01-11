
# HilbertLens 🔬

**HilbertLens** is a diagnostic tool for Quantum Machine Learning (QML). It visualizes the hidden geometry of your quantum encodings and "diagnoses" their capacity to learn complex data.

Instead of blindly training Variational Quantum Circuits (VQC) and guessing why they fail, `HilbertLens` tells you:
1.  **Spectrum Analysis:** Does the circuit have enough bandwidth (expressibility) for the data?
2.  **Geometry Analysis:** Does the encoding preserve the topological structure of the data?

## 📦 Installation

```bash
pip install .

```

For development (so edits are reflected immediately):

```bash
pip install -e .

```

## 🚀 Quick Start

### 1. The "Doctor" Check

Pass your circuit to the `QuantumLens` and ask for a diagnosis.

```python
import hilbertlens as hl
from qiskit.circuit import ParameterVector, QuantumCircuit

# Define your circuit
x = ParameterVector('x', 2)
qc = QuantumCircuit(2)
qc.h([0, 1])
qc.rz(x[0], 0)
qc.rz(x[1], 1)
qc.cx(0, 1) # Entanglement

# Initialize Lens
lens = hl.QuantumLens(qc, params=list(x), framework='qiskit')

# Run Diagnosis (Auto-runs Spectrum and Geometry checks)
lens.diagnose()

```

### 2. Manual Inspection

You can run individual checks and save the plots.

```python
# Check Frequency Spectrum (Capacity)
lens.spectrum(mode='global', save_path="spectrum.png")

# Check Geometry Preservation (using synthetic Swiss Roll)
lens.geometry(save_path="geometry.png")

```

## 🏥 Understanding the Report

* **[GOLD STANDARD]:** Your circuit has a rich spectrum (multiple frequencies) AND preserves geometry. It is ready for research.
* **[SAFE BUT SIMPLE]:** Your circuit is linear (). It will work on simple data (Iris) but underfit complex data (Moons).
* **[BROKEN GEOMETRY]:** Your circuit destroys the data structure (e.g., score < 0.5). Check your data scaling!

## 🔧 Supported Frameworks

* **Qiskit** (Native support)
* **PennyLane** (Auto-detected if installed)


## Sample Output
---
#### Testing with Real Data: Two Moons

**Data Shape:** `(200, 2)`  
**Features:** 2  

#### Quantum Circuit
**Circuit Created:** 2-Qubit Entangled Network


     ┌───┐ ┌──────────┐       ┌──────────┐
q_0: ┤ H ├─┤ Rz(x[0]) ├───■───┤ Rz(x[1]) ├
     ├───┤ ├──────────┤ ┌─┴─┐ ├──────────┤
q_1: ┤ H ├─┤ Rz(x[1]) ├─┤ X ├─┤ Rz(x[0]) ├
     └───┘ └──────────┘ └───┘ └──────────┘


**[HilbertLens]** Initialized for framework: `qiskit`


#### Geometry Check (Two Moons)

**Status:** Analyzing Geometry  
- **Geometry Score (Spearman Correlation):** `0.9182`  
- **Output:** `moons_geometry.png`

---

#### Spectrum Check

**Status:** Computing Spectrum  
**Mode:** Global

### Dominant Frequencies — Global Sweep
- **k = 1.0** | Power: `0.446`  
- **k = 3.0** | Power: `0.442`  
- **k = 2.0** | Power: `0.112`  

**Output:** `moons_spectrum.png`

---

#### HILBERTLENS DIAGNOSIS REPORT

### [1] Spectrum Analysis — Capacity & Expressibility
- **Active Frequencies:** 3 (Richness)  
- **Max Frequency:** `k = 3.0` (Bandwidth)  
- **Category:** High Capacity (Rich Expressibility)  
- **Assessment:** Complex spectrum with three active frequencies; capable of deep nuance.  
- **Advice:** Gold standard. Capable of universal classification.

---

#### [2] Geometry Analysis — Inductive Bias
- **Preservation Score:** `0.9182` (Spearman ρ)  
- **Category:** Excellent Preservation  
- **Assessment:** The quantum kernel faithfully preserves the topological structure of the input data.

---

#### [3] Final Verdict

> **[GOLD STANDARD] READY FOR RESEARCH**  
> Your circuit exhibits **High Capacity (Rich Spectrum)** and **Stable Geometry**.  
> It can learn complex decision boundaries without breaking data topology.
