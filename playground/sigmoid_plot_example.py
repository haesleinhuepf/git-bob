import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    """
    Compute the sigmoid of x.

    Parameters
    ----------
    x : array_like
        Input array or scalar.

    Returns
    -------
    ndarray
        The sigmoid of each element in x.
    """
    return 1 / (1 + np.exp(-x))

# Generate data
x = np.linspace(-10, 10, 100)
y = sigmoid(x)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Sigmoid Function')
plt.title('Sigmoid Function Plot')
plt.xlabel('x')
plt.ylabel('sigmoid(x)')
plt.legend()
plt.grid(True)
plt.show()
