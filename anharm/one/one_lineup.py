import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hgen
import sympy as sp
import cupy as cp

# what is the spectrum of one AHO?
# Do they converge with truncation?
omega = 120
alpha = -1
En = lambda n: omega * n + alpha / 2 * n * (n - 1)
numstates = 50
statess = np.arange(0, numstates, 1)
EE = np.vectorize(En)(statess)
EE = sorted(EE)

H, symbols = Hgen(1, numstates, "line")
hamnum = sp.lambdify(symbols, H, "numpy")
mat = hamnum(omega, alpha)
vals = cp.linalg.eigvalsh(cp.asarray(mat))
vals = cp.asnumpy(vals)

plt.plot(vals, lw=0, marker=".", label="Full")
plt.plot(EE, lw=0, marker=".", label="Diagonal parabola")
plt.title(rf"Energy lineup, AHO 1T, {numstates} states $\alpha$=-1 $\omega$={omega} [-alpha]")
plt.ylabel("E_n")
plt.xlabel("n")
plt.legend()
plt.show()
