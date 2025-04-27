from anharm.Hamiltonian import Hamil
import numpy as np
from matplotlib import pyplot as plt
from other.colormap import Norm, OrBu_colormap
from anharm.Cacher import Cacher

f = Cacher.getzz("1010000", 3, "triang")
alpha = -1
g01 = 0.4
g12 = 0.4
g02 = 0.02

g23 = 0.4
g34 = 0.4
g24 = 0.02

g45 = 0.4
g56 = 0.4
g46 = 0.02

d23 = -2.1
d34 = 1.5


dd13 = np.linspace(-8, 8, 500)
o2prims = np.linspace(-10, 10, 500)

vals = np.zeros((len(dd13), len(o2prims)))
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d12_grid = d2prim_grid + dd13_grid / 2
d01_grid = dd13_grid - d12_grid
vals = f(alpha, alpha, alpha, g01, g12, g02, g23, g24, d01_grid, d12_grid, d23, d34)
print(vals)
plt.pcolormesh(o2prims, dd13_grid, vals, norm=Norm(1e-1), cmap=OrBu_colormap())
plt.title(
    f"ZZ13 $g_{{01}}$={g01} $g_{{12}}$={g12} $g_{{02}}$={g02} $g_{{23}}$={g23} $g_{{34}}$={g34} $g_{{24}}$={g24} $\Delta_{{23}}$={d23} $\Delta_{{34}}$={d34}"
)
plt.xlabel("$\omega_2^\prime$")
plt.ylabel("$\Delta_{13}$")
plt.colorbar()
plt.show()

# TODO: SW cannot do a symmetric sweep so do it numerically
