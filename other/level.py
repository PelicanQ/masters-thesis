import numpy as np
from matplotlib import pyplot as plt

# Plot three level system energies
w = 10
g2 = 1
g1 = np.linspace(-1, 1, 20)


@np.vectorize
def e(g1):
    A = np.array([[-w, g1, 0], [g1, 0, g2], [0, g2, w]])
    vals = np.linalg.eigvalsh(A)
    return vals[0]


ee = e(g1)
plt.plot(g1, ee)
plt.show()
