# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
import inspect
from analysis.discover import make_hoverax_refreshable, make_hoverax, make_mesh

H = Hamil(3, 4, "triang")
e = H.zzexpr("101")
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.19
g23 = 0.19
g13 = 0.003

dd13 = np.linspace(-4, 8, 400)
o2prims = np.linspace(-6, 14, 400)
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid


# @np.vectorize
# def snapto0(v):
#     if np.abs(v) < 1e-5:
#         return 0
#     return v


vals = f(alpha, alpha, alpha, g12, g23, g13, d12_grid, d23_grid)


norm = colors.SymLogNorm(1e-6, vmin=-1e-0, vmax=1e-0)
cmap = OrBu_colormap()


def only():
    plt.figure()
    plt.pcolormesh(d2prim_grid, dd13_grid, vals, norm=norm, cmap=cmap)
    plt.title(rf"ZZ13 $g_{{12}}$={g12} $g_{{23}}$={g23} $g_{{13}}$={g13} $\alpha$={alpha} units [-$\alpha$]")
    plt.xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
    plt.ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    plt.colorbar()
    plt.show()


def decomp():
    pass


if __name__ == "__main__":
    only()
