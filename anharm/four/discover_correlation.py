from anharm.Hamiltonian import Hamil
import sympy as sp
from matplotlib import pyplot as plt, colors
from other.colormap import Norm, OrBu_colormap
import numpy as np
from matplotlib import colors
from analysis.discover import make_discover

H = Hamil(4, 5, "line")
e = H.zzexpr("1111") - (
    H.zzexpr("1100") + H.zzexpr("0110") + H.zzexpr("0011") + H.zzexpr("1010") + H.zzexpr("0101") + H.zzexpr("1001")
)
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
# \alpha_{0}, \alpha_{1}, \alpha_{2}, g_{0,1}, g_{1,2}, g_{0,2}, \Delta_{0,1}, \Delta_{1,2}
g12 = 0.5
g23 = 0.5
g13 = 0.1
dd = np.linspace(-10, 10, 200)
d12, d23 = np.meshgrid(dd, dd)


def calculate(g12, g23, g13):
    Z = f(-1, -1, -1, g12, g23, g13, d12, d23)
    Z = np.abs(Z)
    return Z


ax = make_discover(["g12", "g23", "g13"], [g12, g23, g13], d12, d23, calculate, colors.LogNorm(1e-5, 1e0))
ax.set_xlabel("delta 12")
ax.set_ylabel("delta 23")
ax.set_title(f"|ZZZZ minus all pairs of ZZ| [-alpha]")
plt.show()
