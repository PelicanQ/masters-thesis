from anharm.Hamiltonian import Hamil
import numpy as np
from matplotlib import pyplot as plt
from other.colormap import Norm, OrBu_colormap

H = Hamil(5, 3, "triang")
e = H.zzexpr("10100")
e = H.split_deltas(e)
f, fvars = H.lambdify_expr(e)
print(fvars)
alpha = -1
g01 = 0.4
g12 = 0.4
g23 = 0.4
g34 = 0.4
g02 = 0.02
g24 = 0.02


dd13 = np.linspace(-8, 8, 500)
o2prims = np.linspace(-10, 10, 500)
# translate

vals = np.zeros((len(dd13), len(o2prims)))
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)

d12_grid = d2prim_grid + dd13_grid / 2
d01_grid = dd13_grid - d12_grid


# d23_grid = d12_grid
# d34_grid = d01_grid
d23 = -2.1
d34 = 1.5
vals = f(alpha, alpha, alpha, g01, g12, g02, g23, g24, d01_grid, d12_grid, d23, d34)
print(vals)
plt.pcolormesh(o2prims, dd13_grid, vals, norm=Norm(1e-1), cmap=OrBu_colormap())
plt.title(
    f"ZZ13 $g_{{12}}$={g01} $g_{{23}}$={g12} $g_{{13}}$={g02} $g_{{34}}$={g23} $g_{{35}}$={g24}  $\Delta_{{34}}$={d23} $\Delta_{{45}}$={d34}"
)


plt.xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
plt.ylabel(r"$\Delta_{13}$ [-$\alpha$]")
plt.colorbar()
plt.show()

# TODO: SW cannot do a symmetric sweep so do it numerically
