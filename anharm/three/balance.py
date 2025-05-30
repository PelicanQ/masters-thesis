import numpy as np
from matplotlib import pyplot as plt
from analysis.discover import make_hoverax
from matplotlib import colors
import itertools
from exact.util import exact_energy, to_omega_grid, exact_energy_num
from matplotlib.ticker import MaxNLocator

# what is the net number of levels below?
Ej1s = np.arange(30, 100, 0.5)
Ej2s = np.arange(30, 140, 0.5)
Ej3 = 50
balance_zzz = np.zeros(dtype=int, shape=(len(Ej1s), len(Ej2s)))
balance_zz = np.zeros(dtype=int, shape=(len(Ej1s), len(Ej2s)))


def sorted_vals(Ej1, Ej2, Ej3):
    """Give the sorted bare energies for 3 transmons"""
    C = 30  # TODO run higher
    vals1 = exact_energy_num(1, Ej1, C)
    vals2 = exact_energy_num(1, Ej2, C)
    vals3 = exact_energy_num(1, Ej3, C)
    levels = []
    for comb in itertools.product(range(4), repeat=3):
        n1 = comb[0]
        n2 = comb[1]
        n3 = comb[2]
        if sum(comb) < 4:
            levels.append(((n1, n2, n3), vals1[n1] + vals2[n2] + vals3[n3]))
    levels = sorted(levels, key=lambda item: item[1])
    return levels


def count_net_below(levels, start: int, exc: int):
    above = 0
    for t in range(start + 1, len(levels)):
        if sum(levels[t][0]) == exc:
            above += 1
    below = 0
    for t in range(start - 1, -1, -1):
        if sum(levels[t][0]) == exc:
            below += 1
    return below - above


for i, Ej1 in enumerate(Ej1s):
    print(Ej1)
    for j, Ej2 in enumerate(Ej2s):
        levels = sorted_vals(Ej1, Ej2, Ej3)

        for k in range(len(levels)):
            if levels[k][0] == (1, 1, 1):
                break
        balance_zzz[i, j] = count_net_below(levels, k, 3)

        for k in range(len(levels)):
            if levels[k][0] == (1, 0, 1):
                break
        two_below = count_net_below(levels, k, 2)

        for k in range(len(levels)):
            if levels[k][0] == (1, 0, 0):
                break
        one_below_100 = count_net_below(levels, k, 1)

        for k in range(len(levels)):
            if levels[k][0] == (0, 0, 1):
                break
        one_below_001 = count_net_below(levels, k, 1)
        balance_zz[i, j] = two_below - one_below_100 - one_below_001

o2prim_grid, d13_grid = to_omega_grid(Ej1s, Ej2s, Ej3)

colorz2 = plt.cm.Oranges(np.linspace(0.2, 1, 5))
white = [1, 1, 1, 1]
colorz = np.vstack((plt.cm.Blues_r(0.5), colorz2))
cmap = colors.ListedColormap(colorz)

# Define the boundaries between values:
bounds = np.arange(-2, 11, 2)
norm = colors.BoundaryNorm(bounds, colorz.shape[0])

fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True, sharex=True, figsize=(8, 8), constrained_layout=True)
c1 = make_hoverax(o2prim_grid, d13_grid, balance_zzz, cmap=cmap, norm=norm, ax=ax1)
ax1.set_xlim(-6, 14)

ax1.set_title("Level balances for ZZZ and ZZ")
ax1.set_ylabel(r"$\Delta_{13}$ [$E_C$]")

c2 = make_hoverax(o2prim_grid, d13_grid, balance_zz, cmap=cmap, norm=norm, ax=ax2)
ax2.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
ax2.set_xlabel(r"$\omega_2'$ [$E_C$]")

cbar = fig.colorbar(c1, ax=[ax1, ax2])
cbar.set_ticks([i for i in range(-1, 10, 2)])
plt.show()
