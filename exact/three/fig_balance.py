import numpy as np
from matplotlib import pyplot as plt
from analysis.discover import make_hoverax
from matplotlib import colors
import scienceplots
from exact.util import exact_energy, to_omega_grid, exact_energy_num
from matplotlib.ticker import MaxNLocator

plt.style.use(["science", "nature"])
# what is the net number of levels below?
Ej1s = np.arange(30, 100, 0.5)
Ej2s = np.arange(30, 140, 0.5)
Ej3 = 50
balance_zzz = np.load("balance_zzz.npy")
balance_zz = np.load("balance_zz.npy")

o2prim_grid, d13_grid = to_omega_grid(Ej1s, Ej2s, Ej3)

colorz2 = plt.cm.Oranges(np.linspace(0.2, 1, 5))
white = [1, 1, 1, 1]
colorz = np.vstack((plt.cm.Blues_r(0.5), colorz2))
cmap = colors.ListedColormap(colorz)

# Define the boundaries between values:
bounds = np.arange(-2, 11, 2)
norm = colors.BoundaryNorm(bounds, colorz.shape[0])
fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True, sharex=True, figsize=(5.9 / 2, 5.9 / 2), constrained_layout=True)
c1 = make_hoverax(o2prim_grid, d13_grid, balance_zzz, cmap=cmap, norm=norm, ax=ax1)
ax1.set_xlim(-6, 14)

ax1.set_title("Level balances for ZZZ and ZZ")
ax1.set_ylabel(r"$\Delta_{13}$ [$E_C$]")

c2 = make_hoverax(o2prim_grid, d13_grid, balance_zz, cmap=cmap, norm=norm, ax=ax2)
ax2.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
ax2.set_xlabel(r"$\omega_2'$ [$E_C$]")

cbar = fig.colorbar(c1, ax=[ax1, ax2])
cbar.set_ticks([i for i in range(-1, 10, 2)])
fig.savefig("figs/balance.png", dpi=300, bbox_inches="tight")

plt.show()
