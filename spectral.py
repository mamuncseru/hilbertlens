import numpy as np

def compute_spectrum(kernel_fn, n_samples=1000, range_max=2*np.pi):
    """
    Analyzes the frequency spectrum of a quantum kernel.

    Args:
        kernel_fn (callable): A function that takes a numpy array of shape (N, 1)
                              and returns the kernel matrix (N, N) or vector (N,).
                              We assume K(x, 0) captures the structure.
        n_samples (int): Number of points to sample for the FFT. 
                         Higher = better resolution, less aliasing.
        range_max (float): The interval to sample [0, range_max].
                           For standard Pauli encodings, 2*pi or 4*pi is standard.

    Returns:
        freqs (np.array): The detected integer frequencies (0, 1, 2...).
        power (np.array): The normalized power (importance) of each frequency.
    """
    
    # 1. Create the sweep data
    # We create a linspace of inputs x from 0 to range_max
    # Shape must be (n_samples, 1) to mimic standard ML data shape
    X_sweep = np.linspace(0, range_max, n_samples).reshape(-1, 1)
    
    # 2. Compute the Kernel Signal
    # We compare every point in X_sweep to a fixed reference point (x=0)
    # Ideally, the kernel function should handle K(X, X_ref).
    # If the user's function expects K(X), we might need to handle that.
    # Let's assume for now kernel_fn returns the Gram matrix of the input.
    
    # We pass the sweep data to the kernel function
    K_matrix = kernel_fn(X_sweep)
    
    # We extract the first column: K(x, x[0]) where x[0] = 0.
    # This gives us the function f(x) = K(x, 0)
    signal = K_matrix[:, 0]
    
    # 3. Perform Fourier Transform (FFT)
    # We use rfft because our signal is real-valued (kernel values are real)
    fft_coeffs = np.fft.rfft(signal)
    
    # Calculate the power spectrum (magnitude squared)
    power_spectrum = np.abs(fft_coeffs)**2
    
    # 4. Map FFT indices to real Frequencies
    # The FFT gives us bins. We need to know which integer frequency corresponds to which bin.
    # The resolution of our sampling is sample_spacing = range_max / n_samples
    # The frequency bins correspond to 0, 1/T, 2/T... where T is range_max.
    
    # If we sampled over [0, 2pi], the fundamental frequency is 1.
    # We normalize so that the index corresponds roughly to integer frequencies.
    
    # Get the frequencies corresponding to the FFT bins
    fft_freqs = np.fft.rfftfreq(n_samples, d=(range_max/n_samples))
    
    # We are usually interested in integer frequencies (1x, 2x, 3x...)
    # We will scale the x-axis so that 1.0 means "1 oscillation per 2pi" (if that's our base).
    # Standard convention: If data is angle-encoded, base period is 2pi.
    scale_factor = 2 * np.pi 
    freqs_scaled = fft_freqs * scale_factor
    
    # Normalize power so it sums to 1 (for readability)
    power_normalized = power_spectrum / np.sum(power_spectrum)
    
    return freqs_scaled, power_normalized