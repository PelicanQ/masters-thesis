import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hamil, Hgen
from sim_store.analysis.plot import grid3d, grid_plot2d
import sympy as sp
import cupy as cp
import pandas as pd
from pathlib import Path

# Does the ground level converge with more numstates?
omegas = np.arange(5, 40, 5)
spbs = np.arange(2, 50, 1)
alpha = -1
levels = np.zeros((len(spbs), len(omegas)))

for i, spb in enumerate(spbs):
    H, symbols = Hgen(1, spb, "line")
    hamnum = sp.lambdify(symbols, H, "numpy")
    for io, omega in enumerate(omegas):
        mat = hamnum(omega, alpha)
        vals = cp.linalg.eigvalsh(cp.asarray(mat))
        vals = cp.asnumpy(vals)
        levels[i, io] = vals[0]

stationary_point = np.vectorize(lambda w: 1 / 2 - w / alpha)
turn = np.vectorize(lambda w: 1 - 2 * w / alpha)
lines = stationary_point(omegas)

plt.plot(spbs, levels, label=[rf"$\omega={o}$" for o in omegas])

plt.gca().set_prop_cycle(None)

plt.plot([lines, lines], [-2000, 0], linestyle=":")

plt.title(rf"Convergence of ground, AHO 1T, $\alpha$=-1. ")
plt.xlabel("States per bit")
plt.ylabel("$E_0$ [-alpha]")
plt.legend(loc="lower right")
plt.show()
