# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, my_colors
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from sandbox.util import make_axslid, makeslid
from analysis.discover import make_discover

H = Hamil(3, 4, "triang")
e = H.zzexpr("101")
e = H.split_deltas(e)
f, vars = H.lambdify_expr(e)
print(vars)
alpha = -1
g12 = 0.2
g23 = 0.2
g13 = 0.002

dd13 = np.linspace(-4, 8, 200)
o2prims = np.linspace(-6, 14, 200)
o2_grid, d13_grid = np.meshgrid(o2prims, dd13)
d23_grid = o2_grid + d13_grid / 2
d12_grid = d13_grid - d23_grid


def calculate(g12, g23, g13):
    return f(-1, -1, -1, g12, g23, g13, d12_grid, d23_grid)


@np.vectorize
def snapto0(v):
    if np.abs(v) < 1e-5:
        return 0
    return v


norm = colors.SymLogNorm(1e-6, vmin=-1e0, vmax=1e0)
cmap = OrBu_colormap()


ax = make_discover(["g12", "g23", "g13"], [g12, g23, g13], o2_grid, d13_grid, calculate, norm, cmap)
ax.set_title("ZZ")
plt.show()
