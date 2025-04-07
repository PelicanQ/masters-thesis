import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hamil, Hgen
from sim_store.analysis.plot import grid3d, grid_plot2d
import sympy as sp
import cupy as cp
import pandas as pd
from pathlib import Path

# In the lineup we saw that RWA can approx low energies well
omegas = np.arange(50, 200, 1)
alpha = -1
numstates = 12
num_levels = 8
levels = np.zeros((len(omegas), num_levels))
rwas = np.zeros((len(omegas), num_levels))
En = lambda omega, n: omega * n + alpha / 2 * n * (n - 1)
En = np.vectorize(En)
nn = np.arange(0, num_levels, 1)

H, symbols = Hgen(1, numstates, "line")
hamnum = sp.lambdify(symbols, H, "numpy")

for i, omega in enumerate(omegas):
    # sugg = int(np.ceil(1 / 2 - omega / (2 * alpha)))  # by the heuristic, we choose number of states based on omega
    # print("omega", omega, "num", sugg)
    # if hams[numstates] != None:
    #     hamnum = hams[numstates]
    # else:
    mat = hamnum(omega, alpha)
    vals = cp.linalg.eigvalsh(cp.asarray(mat))
    vals = cp.asnumpy(vals)

    rwalevs = En(omega, nn)
    rwas[i, :] = rwalevs
    levels[i, :] = vals[:num_levels]

diff = levels - rwas
plt.plot(omegas, diff / rwas)
plt.title(rf"Relative error of levels from RWA, AHO 1T, $\alpha$=-1, {numstates} states")
plt.ylabel("Ediff/RWA [-alpha]")
# plt.plot(omegas, levels, marker="")
# plt.gca().set_prop_cycle(None)
# plt.plot(omegas, rwas, linestyle=":")

# plt.title(rf"{num_levels} lowest levels and their RWA, AHO 1T, $\alpha$=-1, {numstates} states")
plt.xlabel("omega [-alpha]")
# plt.ylabel("$E_n$ [-alpha]")
plt.show()
