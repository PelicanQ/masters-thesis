import numpy as np
from matplotlib import pyplot as plt
from analysis.discover import make_hoverax
import itertools
from exact.util import exact_energy, omega_alphas
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from other.colormap import OrBu_colormap

# what is the net number of levels below?

H = Hamil(3, 4, "triang")
e = H.split_deltas(H.zzexpr("111"))
f, vars = H.lambdify_expr(e)
alpha = -1
g12 = 0.19
g23 = 0.19
g13 = 0.003
V = 8
H = 5
dd13 = np.linspace(-V, V, 500)
oo2 = np.linspace(-H, H, 500)
o2grid, d13grid = np.meshgrid(oo2, dd13)

d23grid = o2grid + d13grid / 2
d12grid = d13grid - d23grid

alpha = 1

norm = colors.SymLogNorm(1e-6, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()
Z = f(-1, -1, -1, g12, g23, g13, d12grid, d23grid)
plt.pcolormesh(o2grid, d13grid, Z * 0.00001, cmap=cmap, norm=norm)


def centered_text(x, y, text, **kwargs):
    plt.text(x, y, text, ha="center", va="center", fontsize=11, **kwargs)


centered_text(3, 0.7, r"$\omega_{2}>\omega_1 + |\alpha|$")
centered_text(3, -0.7, r"$\omega_{2}>\omega_3 + |\alpha|$")
centered_text(-3, -0.7, r"$\omega_{2}-\omega_1< -|\alpha|$")
centered_text(-3, 0.7, r"$\omega_{2}-\omega_3< - |\alpha|$")

centered_text(0, 7, r"$\omega_{3}+|\alpha| < \omega_2 < \omega_{1}-|\alpha|$")
centered_text(0, -7, r"$\omega_{1}+|\alpha| < \omega_2 < \omega_{3}-|\alpha|$")

plt.plot(dd13, 2 * (dd13 + alpha), color="black")
plt.plot(dd13, 2 * (dd13 - alpha), color="black")
plt.plot(dd13, 2 * (-dd13 + alpha), color="black")
plt.plot(dd13, 2 * (-dd13 - alpha), color="black")
plt.xlabel("o2 prim [-alpha]")
plt.ylabel("d13 [-alpha]")

plt.title("Yani")
plt.xlim(-H, H)
plt.ylim(-V, V)


plt.show()
