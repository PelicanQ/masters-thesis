import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hamil, Hgen
from analysis.plot import grid3d, grid_plot2d
import sympy as sp
import cupy as cp
import pandas as pd
from pathlib import Path

# Let's see how a few levels vary with numstates
omega = 20
spbs = np.arange(8, 30, 1)
num_levels = 8
alpha = -1
levels = np.zeros((len(spbs), num_levels))

for i, spb in enumerate(spbs):
    H, symbols = Hgen(1, spb, "line")
    hamnum = sp.lambdify(symbols, H, "numpy")
    mat = hamnum(omega, alpha)
    vals = cp.linalg.eigvalsh(cp.asarray(mat))
    vals = cp.asnumpy(vals)
    levels[i, :] = vals[:num_levels]

# levels = (levels.T - levels[:, -1].T).T  # relative to each final vals
plt.plot(spbs, levels, marker="")
plt.title(rf"Convergence of levels, AHO 1T, $\alpha$=-1 $\omega$={omega} [-alpha]")
plt.xlabel("States per bit")
plt.ylabel("$E_n$ [-alpha]")
plt.show()
