import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hgen
from analysis.plot import grid3d, grid_plot2d
import sympy as sp
import cupy as cp
import pandas as pd

# Does the ground level converge with more numstates?
omega = 30
spbs = np.arange(5, 18, 1)
alpha = -1
levels = np.zeros((len(spbs),))

for i, spb in enumerate(spbs):
    H, symbols = Hgen(1, spb, "line")
    hamnum = sp.lambdify(symbols, H, "numpy")
    mat = hamnum(omega, alpha)
    vals = cp.linalg.eigvalsh(cp.asarray(mat))
    vals = cp.asnumpy(vals)
    levels[i] = vals[0]


plt.plot(spbs, levels)

# plt.plot([turns, turns], [-2000, 0], linestyle=":")

plt.title(rf"Convergence of ground, AHO 1T, omega=30[-alpha] $\alpha$=-1. ")
plt.xlabel("States per bit")
plt.ylabel("$E_0$ [-alpha]")
plt.legend()
plt.show()
