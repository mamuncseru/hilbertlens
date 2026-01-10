import matplotlib.pyplot as plt
import numpy as np
import os

def plot_spectrum(freqs, power, top_k=5, title="Quantum Kernel Spectrum", save_path=None):
    """
    Visualizes the frequency spectrum.
    
    Args:
        freqs (array): The frequency integers/floats (k).
        power (array): The normalized power.
        top_k (int): How many top frequencies to label explicitly.
        save_path (str, optional): Full path (including filename) to save the plot. 
                                   If None, the plot is displayed interactively.
    """
    fig = plt.figure(figsize=(10, 6))
    
    # Plot the full spectrum as a bar chart (stem plot)
    # We limit x-axis because quantum models usually have low frequencies.
    # Showing 0 to 10 is usually enough for visualization.
    mask = freqs <= 10.0
    plt.stem(freqs[mask], power[mask], basefmt=" ", linefmt='b-', markerfmt='bo')
    
    plt.xlabel(r"Frequency $k$ (in $e^{ikx}$)")
    plt.ylabel("Spectral Power")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    # Annotate the top K frequencies
    # Sort by power descending
    sorted_indices = np.argsort(power)[::-1]
    
    print(f"\n--- Dominant Frequencies for: {title} ---")
    for i in range(top_k):
        if i >= len(sorted_indices): break
        
        idx = sorted_indices[i]
        f = freqs[idx]
        p = power[idx]
        
        # Only label if significant (power > 1%)
        if f <= 10.0 and p > 0.01: 
            plt.text(f, p, f" k={f:.1f}\n", ha='center', va='bottom', fontweight='bold', fontsize=9)
            print(f"Freq k={f:.1f} | Power: {p:.3f}")
    plt.ylim(0, 1.15)        
    plt.tight_layout()
    
    if save_path:
        # Ensure directory exists
        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")
        plt.close(fig) # Close figure to free memory
    else:
        plt.show()