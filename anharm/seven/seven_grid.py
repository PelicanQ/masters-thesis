from anharm.Hamiltonian import Hamil
import numpy as np
from matplotlib import pyplot as plt
from other.colormap import Norm, OrBu_colormap
from anharm.Cacher import Cacher

f = Cacher.getzz("1010000", 3, "grid")  # alpha0 alpha1 alpha2 g01 g12 g02 g23 g24 g25 g26 d01 d12 d23 d34 d45 d56
alpha = -1
g01 = 0.4
g12 = 0.4
g02 = 0.02

g23 = 0.4
g24 = 0.02
g25 = 0.02
g26 = 0.02

d23 = -2.1
d34 = 1.5

d25 = 0.7  # special
d56 = -0.4

d45 = d25 - d23 - d34

dd13 = np.linspace(-8, 8, 500)
o2prims = np.linspace(-10, 10, 500)

vals = np.zeros((len(dd13), len(o2prims)))
d2prim_grid, dd13_grid = np.meshgrid(o2prims, dd13)
d12_grid = d2prim_grid + dd13_grid / 2
d01_grid = dd13_grid - d12_grid
vals = f(alpha, alpha, alpha, g01, g12, g02, g23, g24, g25, g26, d01_grid, d12_grid, d23, d34, d45, d56)

plt.pcolormesh(o2prims, dd13_grid, vals, norm=Norm(1e-1), cmap=OrBu_colormap())
plt.title(rf"$ZZ_{{13}}$ g=({g01},{g12},{g02},{g23},{g24},{g25},{g26}) $\Delta=({d23},{d34},{d25},{d56})$ [-$\alpha$]")
plt.xlabel(r"$\omega_2^\prime$ [-$\alpha$]")
plt.ylabel(r"$\Delta_{13}$ [-$\alpha$]")
plt.colorbar()
plt.show()

# TODO: SW cannot do a symmetric sweep so do it numerically
