from anharm.Hamiltonian import Hamil
import sympy as sp
from matplotlib import pyplot as plt, colors
from other.colormap import Norm, OrBu_colormap
import numpy as np
from matplotlib import colors
from analysis.discover import make_discover

H = Hamil(3, 4, "triang")
e = H.split_deltas(H.zzexpr("111") - (H.zzexpr("110") + H.zzexpr("101") + H.zzexpr("011")))
e_zzz = H.split_deltas(H.zzexpr("111"))
f, _ = H.lambdify_expr(e)
f_zzz, vars_zzz = H.lambdify_expr(e_zzz)
# \alpha_{0} \alpha_{1} \alpha_{2} g_{0,1} g_{1,2} g_{0,2} \Delta_{0,1} \Delta_{1,2}
# \alpha_{0} \alpha_{1} \alpha_{2} g_{0,1} g_{1,2} g_{0,2} \Delta_{0,1} \Delta_{1,2}


def deltas():
    g12 = 0.5
    g23 = 0.5
    g13 = 0.02
    dd = np.linspace(-10, 10, 200)
    d12, d23 = np.meshgrid(dd, dd)

    def calculate(g12, g23, g13):
        Z = f(-1, -1, -1, g12, g23, g13, d12, d23)
        return np.abs(Z) / np.abs(f_zzz(-1, -1, -1, g12, g23, g13, d12, d23))

    ax = make_discover(["g12", "g23", "g13"], [g12, g23, g13], d12, d23, calculate, colors.LogNorm(1e-6, 1e2))
    ax.set_xlabel("delta 12 [-alpha]")
    ax.set_ylabel("delta 23 [-alpha]")
    ax.set_title(r"$\frac{|ZZZ - (ZZ's)|}{|ZZZ|}$")
    plt.show()


def gs():
    g13 = 0
    d12 = 0.6
    d23 = 1.2
    gg = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(gg, gg)

    def calculate(d12, d23):
        Z = f(-1, -1, -1, X, Y, g13, d12, d23)
        Z = np.abs(Z)
        return Z

    ax = make_discover(["d12", "d23"], [d12, d23], X, Y, calculate, colors.LogNorm(1e-6, 1e0))
    ax.set_xlabel("g12")
    ax.set_ylabel("g23")
    ax.set_title(f"|ZZZ minus all pairs of ZZ| g13=0 [-alpha]")
    plt.show()


if __name__ == "__main__":
    deltas()
