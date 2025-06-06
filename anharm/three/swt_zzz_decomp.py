# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
import inspect
from analysis.discover import make_hoverax
import scienceplots

plt.style.use(["science", "nature"])

H = Hamil(3, 4, "triang")
e = H.split_deltas(H.zzexpr("111"))
f_zzz, vars = H.lambdify_expr(e)

alpha = -1
g12 = 0.19
g23 = 0.19
g13 = 0.003

dd13 = np.linspace(-8, 8, 500)
o2prims = np.linspace(-14, 14, 500)
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d23_grid = d2prim_grid + dd13_grid / 2
d12_grid = dd13_grid - d23_grid


norm = colors.SymLogNorm(1e-6, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()


def zzzfunctions():
    s = H.get_subspace(3)

    e1 = s.get_edge("111", "021") + s.get_all_edge_corrections("111", "021")
    e2 = s.get_edge("111", "201") + s.get_all_edge_corrections("111", "201")
    e3 = s.get_4loop_contraction("111", "021") + s.get_4loop_contraction("111", "201")
    group01 = e1 + e2 + e3
    e1 = s.get_edge("111", "120") + s.get_all_edge_corrections("111", "120")
    e2 = s.get_edge("111", "102") + s.get_all_edge_corrections("111", "102")
    e3 = s.get_4loop_contraction("111", "120") + s.get_4loop_contraction("111", "102")
    group12 = e1 + e2 + e3
    e1 = s.get_edge("111", "210") + s.get_all_edge_corrections("111", "210")
    e2 = s.get_edge("111", "012") + s.get_all_edge_corrections("111", "012")
    e3 = s.get_4loop_contraction("111", "210") + s.get_4loop_contraction("111", "012")
    group02 = e1 + e2 + e3
    group3 = s.get_3cycles("111")
    group4 = (
        s.get_4loop_contraction("111", "003")
        + s.get_4loop_contraction("111", "030")
        + s.get_4loop_contraction("111", "300")
    )

    group01 = H.split_deltas(group01)
    group12 = H.split_deltas(group12)
    group02 = H.split_deltas(group02)
    group3 = H.split_deltas(group3)
    group4 = H.split_deltas(group4)

    f01, vars01 = H.lambdify_expr(group01)
    f12, vars12 = H.lambdify_expr(group12)
    f02, vars02 = H.lambdify_expr(group02)
    f3, vars3 = H.lambdify_expr(group3)
    f4, vars4 = H.lambdify_expr(group4)
    print(vars01)
    print(vars12)
    print(vars02)
    print(vars3)
    print(vars4)
    return f01, f12, f02, f3, f4


def decomp():
    f01, f12, f02, f3, f4 = zzzfunctions()

    def calculate(alpha, g12, g23, g13, d12, d23):
        args = (alpha, alpha, alpha, g12, g23, g13, d12, d23)
        return f_zzz(*args), f01(*args), f12(*args), f02(*args), f3(*args), f4(*args)

    vals, vals01, vals12, vals02, vals3, vals4 = calculate(alpha, g12, g23, g13, d12_grid, d23_grid)

    fig = plt.figure(constrained_layout=True, figsize=(5.9, 5.9 * 3 / 4))
    ((ax1, ax2, ax3), (ax4, ax5, ax6)) = fig.subplots(2, 3, sharex=True, sharey=True)
    fig.suptitle(
        rf"Grouped contributions to ZZZ $g_{{12}}$={g12} $g_{{23}}$={g23} $g_{{13}}$={g13} $\alpha$={alpha} units [-$\alpha$]"
    )

    c1 = make_hoverax(d2prim_grid, dd13_grid, vals, norm=norm, cmap=cmap, ax=ax1)
    # ax1.set_title("ZZZ")

    c2 = make_hoverax(d2prim_grid, dd13_grid, vals01, norm=norm, cmap=cmap, ax=ax2)
    # ax2.set_title("01")

    c3 = make_hoverax(d2prim_grid, dd13_grid, vals12, norm=norm, cmap=cmap, ax=ax3)
    # ax3.set_title("12")

    c4 = make_hoverax(d2prim_grid, dd13_grid, vals02, norm=norm, cmap=cmap, ax=ax4)
    # ax4.set_title("02")

    c5 = make_hoverax(d2prim_grid, dd13_grid, vals3, norm=norm, cmap=cmap, ax=ax5)
    # ax5.set_title("3loops")

    c6 = make_hoverax(d2prim_grid, dd13_grid, vals4, norm=norm, cmap=cmap, ax=ax6)
    # ax6.set_title("Residual 4-contractions")

    fig.colorbar(c1, ax=[ax1, ax2, ax3, ax4, ax5, ax6], fraction=0.05)
    ax1.set_ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    ax4.set_ylabel(r"$\Delta_{13}$ [-$\alpha$]")
    ax4.set_xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
    ax5.set_xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
    ax6.set_xlabel(r"$\omega_2^\prime$ [-$\alpha$]")

    fig.savefig("figs/swt-zzz-recreate-decomp.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    decomp()
