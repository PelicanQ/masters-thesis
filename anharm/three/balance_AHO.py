import numpy as np
from matplotlib import pyplot as plt
from analysis.discover import make_hoverax
from matplotlib import colors
import itertools
from exact.util import exact_energy, to_omega_grid
from matplotlib.ticker import MaxNLocator

# what is the net number of levels below?

dd13 = np.linspace(-8, 8, 400)
o2prims = np.linspace(-14, 14, 400)
o2_grid, d13_grid = np.meshgrid(o2prims, dd13)
d23_grid = o2_grid + d13_grid / 2
d12_grid = d13_grid - d23_grid

balance_zzz = np.zeros(dtype=int, shape=(len(dd13), len(o2prims)))
balance_zz = np.zeros(dtype=int, shape=(len(dd13), len(o2prims)))
alpha = -1


def sorted_vals(d12, d23):
    o1 = d12 + d23
    o2 = d23
    o3 = 0
    """Give the sorted bare energies for 3 transmons"""
    vals1 = [0, o1, 2 * o1 + alpha, 3 * o1 + 3 * alpha]
    vals2 = [0, o2, 2 * o2 + alpha, 3 * o2 + 3 * alpha]
    vals3 = [0, o3, 2 * o3 + alpha, 3 * o3 + 3 * alpha]
    list = []
    for comb in itertools.product(range(4), repeat=3):
        n1 = comb[0]
        n2 = comb[1]
        n3 = comb[2]
        if sum(comb) < 4:
            list.append(((n1, n2, n3), vals1[n1] + vals2[n2] + vals3[n3]))
    list = sorted(list, key=lambda item: item[1])
    levels = [x[0] for x in list]
    states = [x[1] for x in list]
    return levels, states


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


for i in range(len(o2prims)):
    for j in range(len(dd13)):
        o1 = d12_grid[i, j] + d23_grid[i, j]
        o2 = d23_grid[i, j]
        o3 = 25
        levels_list = sorted_vals(o1, o2, o3)

        for k in range(len(levels_list)):
            if levels_list[k][0] == (1, 1, 1):
                break
        balance_zzz[i, j] = count_net_below(levels_list, k, 3)

        for k in range(len(levels_list)):
            if levels_list[k][0] == (1, 0, 1):
                break
        two_below = count_net_below(levels_list, k, 2)

        for k in range(len(levels_list)):
            if levels_list[k][0] == (1, 0, 0):
                break
        one_below_100 = count_net_below(levels_list, k, 1)

        for k in range(len(levels_list)):
            if levels_list[k][0] == (0, 0, 1):
                break
        one_below_001 = count_net_below(levels_list, k, 1)
        balance_zz[i, j] = two_below - one_below_100 - one_below_001

o2prim_grid, d13_grid = to_omega_grid(o1s, o2s, Ej3)

colorz2 = plt.cm.Oranges(np.linspace(0.2, 1, 5))
white = [1, 1, 1, 1]
colorz = np.vstack((plt.cm.Blues_r(0.5), colorz2))
cmap = colors.ListedColormap(colorz)

# Define the boundaries between values:
bounds = np.arange(-2, 11, 2)
norm = colors.BoundaryNorm(bounds, colorz.shape[0])

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6), constrained_layout=True)
c1 = make_hoverax(o2prim_grid, d13_grid, balance_zzz, cmap=cmap, norm=norm, ax=ax1)

ax1.set_xlabel("o2 prim [-alpha]")
ax1.set_ylabel("d13 [-alpha]")
ax1.set_title("E111 level balance in 3 exc")
ax1.set_xlim(-6, 14)

c2 = make_hoverax(o2prim_grid, d13_grid, balance_zz, cmap=cmap, norm=norm, ax=ax2)
ax2.set_title("zz13 2 exc balance")
ax2.set_xlabel("o2 prim [-alpha]")
ax2.set_xlim(-6, 14)

cbar = fig.colorbar(c1, ax=[ax1, ax2])
cbar.set_ticks([i for i in range(-1, 10, 2)])
plt.show()
