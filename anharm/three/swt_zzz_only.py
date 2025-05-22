# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
import inspect
from analysis.discover import make_hoverax

H = Hamil(3, 4, "triang")
e = H.split_deltas(H.zzexpr("111"))
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.19
g23 = 0.19
g13 = 0.003

dd13 = np.linspace(-4, 8, 500)
o2prims = np.linspace(-6, 14, 500)
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid


norm = colors.SymLogNorm(1e-6, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()


def only():
    vals = f(alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)
    fig, ax, c, cbar = make_hoverax(d2prim_grid, dd13_grid, vals, norm=norm, cmap=cmap)
    ax.set_title(rf"ZZZ $g_{{12}}$={g12} $g_{{23}}$={g23} $g_{{13}}$={g13} $\alpha$={alpha} units [-$\alpha$]")
    ax.set_xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
    ax.set_ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    plt.show()


if __name__ == "__main__":
    only()
