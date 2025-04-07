import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from anharm.Subspace import Hamil
import sympy as sp
import cupy as cp
import pandas as pd
import pandasgui
import dill
from pathlib import Path

# y = [5, 15.1, 25.8, 37.4, 48.9, 60.8, 72.8, 84.9]


# # y = [2.3, 7, 13, 18.57, 24.28, 30.34, 36.3, 42.5, 48.5]
# x = [5, 10, 15, 20, 25, 30, 35, 40]

# r = np.polyfit(x, y, 1)

# print(r)
# plt.plot(x, y, marker=".")
# plt.xlabel("states per bit")
# plt.ylabel("omega1[g] at dip")
# plt.title("Dip dependence on states per bit, alpha1=alpha2=-2[g] omega2=30[g] (independent of omega2)")
# plt.show()
# exit()
base = Path(__file__).parent
# I want to find energies of the anharmonic model
# with and without RWA comparison
statesperbit = 20
# Ham = Hamil(2, statesperbit, "line")
# hamnum = Ham.lambdify()

# with open((base / f"lam{statesperbit}").resolve(), "wb") as f:
#     f.write(dill.dumps(hamnum))
# exit()
with open((base / f"lam{statesperbit}").resolve(), "rb") as f:
    r = f.read()
    hamnum = dill.loads(r)
# aa = hamnum(30, 30, -1, -1, 1, 1)
# print(np.linalg.cond(aa))
# pandasgui.show(pd.DataFrame(aa[-20:, -20:]))
# exit()
g12 = g23 = 1  # unit 1
omegas = np.linspace(10, 40, 40)  # as seen, Eint below 1 should well cover the relevant
num_levels = 20
levels = np.zeros(shape=(num_levels, len(omegas)))

for i, omega in enumerate(omegas):
    print(i)
    mat = hamnum(omega, 30, -1, -1, 1, 1)
    vals = cp.linalg.eigvalsh(cp.asarray(mat))
    vals = cp.asnumpy(vals)
    levels[:, i] = vals[:num_levels] - vals[0]


plt.plot(omegas, levels.T)
plt.title(
    r"16 lowest levels of anharmonic 2T model, $\omega_2=30$ [g] $\alpha_1=\alpha_2=-1$ [g], $g_{12}=g_{23}=1$ [g]"
)
plt.xlabel("$\omega_1$ [g]")
plt.ylabel("$E_n$ [g]")
plt.show()
