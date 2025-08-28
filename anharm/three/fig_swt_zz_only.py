# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
import initplots

H = Hamil(3, 4, "triang")
e = H.zzexpr("101")
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.19
g23 = 0.19
g13 = 0.003

dd13 = np.linspace(-8, 8, 1000)
o2prims = np.linspace(-14, 14, 1000)
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid


vals = f(alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)


norm = colors.SymLogNorm(1e-6, vmin=-1e-0, vmax=1e-0)
cmap = OrBu_colormap()


def only():
    plt.figure(constrained_layout=True, figsize=(5.9 * 0.8, 5.9 * 3 / 4 * 0.8))
    plt.pcolormesh(d2prim_grid, dd13_grid, vals, norm=norm, cmap=cmap, rasterized=True)
    # plt.title(rf"$\text{{ZZ}}_{{13}}$ for $g_{{12}}=g_{{23}}={g12}$, $g_{{13}}$={g13} units [-$\alpha$]")
    plt.xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
    plt.ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    cbar = plt.colorbar()
    cbar.set_label(r"$\text{ZZ}_{13}$ [$E_C$]")
    plt.savefig("figs/zz13-recreate.pdf", bbox_inches="tight", dpi=300)
    plt.show()


def decomp():
    pass


if __name__ == "__main__":
    only()
