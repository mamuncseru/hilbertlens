import numpy as np
from qiskit.quantum_info import Statevector

# We try-import pennylane to make it an optional dependency
try:
    import pennylane as qml
    HAS_PENNYLANE = True
except ImportError:
    HAS_PENNYLANE = False

class QiskitAdapter:
    def __init__(self, circuit, data_params, use_gpu=False):
        """
        Wraps a Qiskit circuit to behave like a Kernel function.
        
        Args:
            circuit (QuantumCircuit): The Qiskit circuit ansatz.
            data_params (list or Parameter): The parameter(s) in the circuit 
                                            that represent input data 'x'.
        """
        self.circuit = circuit
        
        # Ensure data_params is a list
        if not isinstance(data_params, list):
            self.data_params = [data_params]
        else:
            self.data_params = data_params
            
    def get_kernel_matrix(self, X):
        """
        Computes the kernel matrix for input data X.
        K(x, y) = |<psi(x)|psi(y)>|^2
        
        Args:
            X (array): Input data of shape (N, d). 
                       d must match len(data_params).
        
        Returns:
            K (array): (N, N) kernel matrix.
        """
        # Ensure X is 2D
        if X.ndim == 1:
            X = X.reshape(-1, 1)
            
        N = X.shape[0]
        state_vectors = []
        
        # 1. Generate Statevectors for each data point
        # This loop binds the data 'x' to the circuit parameters
        for i in range(N):
            # Create a dictionary {Parameter: value}
            param_values = {p: X[i, j] for j, p in enumerate(self.data_params)}
            
            # Bind parameters to a new circuit
            bound_circuit = self.circuit.assign_parameters(param_values)
            
            # Simulate to get the statevector |psi(x)>
            sv = Statevector(bound_circuit).data
            state_vectors.append(sv)
            
        # 2. Compute the Gram Matrix (Inner Products)
        # Stack vectors into a matrix M of shape (N, 2^qubits)
        M = np.array(state_vectors)
        
        # Compute M @ M_conjugate_transpose
        # This gives us the inner products <psi(x) | psi(y)> for all pairs
        inner_products = M @ M.conj().T
        
        # The kernel is the magnitude squared: |<psi|psi>|^2
        kernel_matrix = np.abs(inner_products)**2
        
        return kernel_matrix
    

class PennyLaneAdapter:
    def __init__(self, qnode):
        """
        Wraps a PennyLane QNode to behave like a Kernel function.
        
        Args:
            qnode (qml.QNode): A PennyLane QNode. It MUST:
                               1. Take the data 'x' as its FIRST argument.
                               2. Return qml.state().
        """
        if not HAS_PENNYLANE:
            raise ImportError("PennyLane is not installed. Run 'pip install pennylane'.")
            
        self.qnode = qnode

    def get_kernel_matrix(self, X):
        """
        Computes the kernel matrix for input data X.
        """
        # Ensure X is 2D (N, d) or (N, 1)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
            
        N = X.shape[0]
        state_vectors = []
        
        # 1. Compute States
        # PennyLane is usually slower at batching than Qiskit, so we loop.
        for i in range(N):
            # We assume the QNode takes the vector x as the first argument.
            # We flatten it because QNodes often expect 1D arrays or scalars.
            row = X[i].flatten()
            
            # If it's a single feature, pass as scalar; otherwise pass array
            if len(row) == 1:
                val = row[0]
            else:
                val = row
                
            state = self.qnode(val)
            
            # PennyLane returns a tensor, convert to numpy
            if hasattr(state, "numpy"):
                state = state.numpy()
                
            state_vectors.append(state)
            
        # 2. Compute Gram Matrix
        M = np.array(state_vectors)
        # Inner products: M @ M_conjugate_transpose
        inner_products = M @ M.conj().T
        kernel_matrix = np.abs(inner_products)**2
        
        return kernel_matrix