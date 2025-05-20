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
g12 = 0.5
g23 = 0.5
g13 = 0.02

dd13 = np.linspace(-8, 8, 200)
o2prims = np.linspace(-8, 8, 200)
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


norm = colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1)
cmap = OrBu_colormap()


ax = make_discover(["g12", "g23", "g13"], [g12, g23, g13], o2_grid, d13_grid, calculate, norm, cmap)
ax.set_title("ZZ")
plt.show()
