import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_distribution(mean=0, std_dev=1, num_samples=1000):
    """
    Plot a normal distribution with specified mean and standard deviation.

    Parameters
    ----------
    mean : float, optional
        The mean of the normal distribution. Default is 0.
    std_dev : float, optional
        The standard deviation of the normal distribution. Default is 1.
    num_samples : int, optional
        The number of sample points to plot. Default is 1000.

    Returns
    -------
    None
    """
    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, num_samples)
    y = norm.pdf(x, mean, std_dev)
    
    plt.plot(x, y, label=f'Normal Distribution (mean={mean}, std={std_dev})')
    plt.title('Normal Distribution')
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    plot_normal_distribution()
