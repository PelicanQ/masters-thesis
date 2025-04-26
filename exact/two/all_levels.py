from .hamil import eig_clever
import numpy as np
from matplotlib import pyplot as plt

dd = np.arange(40, 60, 1)
k = 15
N = 2 * k + 1  # transmon states per subspace
L = np.zeros((N**2, len(dd)))
for j, d in enumerate(dd):
    levels, vecs, idx_map = eig_clever(Ej1=d, k=k, Ej2=50)
    L[:, j] = levels

plt.plot(dd, L.T)
plt.title(f"All {N**2} levels, k={k}")
plt.xlabel("Ej1 [Ec]")
plt.ylabel(f"E [Ec]")
plt.show()
