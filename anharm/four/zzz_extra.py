# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from anharm.four.makezz import getextrazz13
from analysis.discover import make_discover

H = Hamil(4, 3, "4")
e = H.split_deltas(getextrazz13(H))
e = H.combine_deltas(e, [(0, 1, 2)])
f, vars = H.lambdify_expr(e)  # [\alpha_{0}, \alpha_{2}, g_{0,2}, g_{2,3}, \Delta_{0,2}, \Delta_{2,3}]
alpha = -1
g13 = 0.4
g34 = 0.3

dd13 = np.linspace(-10, 10, 200)
dd34 = np.linspace(-10, 10, 200)
dd34_grid, dd13_grid = np.meshgrid(dd34, dd13)


@np.vectorize
def snapto0(v):
    if np.abs(v) < 1e-5:
        return 0.0
    return v


def calc(*, g13, g34):
    val_mat = f(alpha, alpha, g13, g34, dd13_grid, dd34_grid)
    return val_mat


norm = colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1)
cmap = OrBu_colormap()


def only():
    ax = make_discover(["g13", "g34"], [g13, g34], dd34_grid, dd13_grid, calc, norm, cmap)
    # plt.pcolormesh(dd34_grid, dd13_grid, f(alpha, alpha, g13, g34, dd13_grid, dd34_grid), norm=norm, cmap=cmap)
    ax.set_title(rf"extra ZZ13 4T units [-$\alpha$]")
    ax.set_xlabel(r"$\Delta_{34}$ [-$\alpha$]")
    ax.set_ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    plt.show()


if __name__ == "__main__":
    only()
