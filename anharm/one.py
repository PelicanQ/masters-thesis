import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from anharm.Subspace import Hamil, Hgen
import sympy as sp
import cupy as cp
import pandas as pd
import pandasgui
import dill
from pathlib import Path

# what is the spectrum of one AHO? Let's plot a few levels vs omega
# Do they converge with truncation?
base = Path(__file__).parent
statesperbit = 10
H, symbols = Hgen(1, statesperbit, "line")
hamnum = sp.lambdify(symbols, H, "numpy")
print(symbols)
omegas = np.linspace(0, 40, 40)  # as seen, Eint below 1 should well cover the relevant
num_levels = statesperbit
levels = np.zeros(shape=(num_levels, len(omegas)))
alpha = -1
for i, omega in enumerate(omegas):
    mat = hamnum(omega, alpha)
    vals = cp.linalg.eigvalsh(cp.asarray(mat))
    vals = cp.asnumpy(vals)
    levels[:, i] = vals[:num_levels] - vals[0]


plt.plot(omegas, levels.T)
plt.title(r"Levels of AHO 1T model, $\alpha=-1$")
plt.xlabel("$\omega$ [-alpha]")
plt.ylabel("$E_n - E_0$ [-alpha]")
plt.show()
