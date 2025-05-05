# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from anharm.four.makezz import getextrazz13
from analysis.discover import make_discover

H = Hamil(4, 4, "4")
e = H.split_deltas(H.zzexpr("1110"))
f, vars = H.lambdify_expr(e)
# \alpha_{0}, \alpha_{1}, \alpha_{2}, g_{0,1}, g_{1,2}, g_{0,2}, g_{2,3}, \Delta_{0,1}, \Delta_{1,2}, \Delta_{2,3}
alpha = -1
g12 = 0.4
g23 = 0.4
g13 = 0.05
g34 = 0.4
d34 = 1.1

dd13 = np.linspace(-10, 10, 400)
o2prim = np.linspace(-10, 10, 400)
o2prim_grid, dd13_grid = np.meshgrid(o2prim, dd13)
d23_grid = o2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid


@np.vectorize
def snapto0(v):
    if np.abs(v) < 1e-5:
        return 0.0
    return v


def calc(*, g12, g23, g13, g34, d34):
    val_mat = f(alpha, alpha, alpha, g12, g23, g13, g34, d12_grid, d23_grid, d34)
    return snapto0(val_mat)


norm = colors.SymLogNorm(1e-5, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()


def only():
    ax = make_discover(
        ["g12", "g23", "g13", "g34", "d34"], [g12, g23, g13, g34, d34], o2prim_grid, dd13_grid, calc, norm, cmap
    )
    # plt.pcolormesh(dd34_grid, dd13_grid, f(alpha, alpha, g13, g34, dd13_grid, dd34_grid), norm=norm, cmap=cmap)
    ax.set_title(rf"ZZZ 4T units [-$\alpha$]")
    ax.set_ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    ax.set_xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
    plt.show()


if __name__ == "__main__":
    only()
