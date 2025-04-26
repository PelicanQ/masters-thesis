from .hamil import calc_eig
from analysis.levels import grid_plot, grid_plot2d
from matplotlib import pyplot as plt
import numpy as np

# Energy conv for different Eint
# Eints = [0.1, 0.5, 1, 5, 10, 50]
kk = [5, 7, 9, 11, 12, 15, 18, 20, 24, 28, 32, 36, 40, 50, 60, 70]
# Eints = [0.1, 0.5]
# kk = [5, 7, 9, 11, 12, 15]
# collection = []
# stds = []
# for Eint in Eints:
convlist = []
for k in kk:
    vals = calc_eig(Ej=10, Eint=5, k=k)
    E = vals[0]
    convlist.append(E)

std = np.std(convlist[5:])

plt.plot(kk, convlist, marker=".")
plt.xlabel("k")
plt.ylabel("E0")
plt.title(f"Extended converge, Eint=5, Ej=10, std=1e{np.log10(std):.0f} at=15")
plt.show()
# collection.append(convlist)

# low_cut = 5
# grid_plot2(
#     kk,
#     collection,
#     Eints,
#     (2, 3),
#     "k",
#     "E0",
#     "Ground level, varying Eint, Ej=10, std cut 15",
#     "Eint",
#     stds,
# )

# Energy lineup for different Eint
# Eints = [10, 20, 50, 100, 200, 500]
# collection = []
# for Eint in Eints:
#     vals = calc_eig(Ej=10, Eint=Eint, k=36)[:50]
#     collection.append(vals)

# grid_plot(
#     collection,
#     Eints,
#     (2, 3),
#     "n",
#     "En",
#     "All energies, varying Eint, Ej=10, k=36",
#     "Eint",
# )
