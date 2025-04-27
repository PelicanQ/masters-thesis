# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, my_colors
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from sandbox.util import make_axslid, makeslid
from anharm.Cacher import Cacher
from analysis.discover import make_hoverax_refreshable


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
d45 = 1.5
d56 = -1


dd02 = np.linspace(-8, 8, 200)
o1prims = np.linspace(-10, 10, 200)


d1prim_grid, dd02_grid = np.meshgrid(o1prims, dd02)
d12_grid = d1prim_grid + dd02_grid / 2
d01_grid = dd02_grid - d12_grid


@np.vectorize
def snapto0(v):
    if np.abs(v) < 1e-5:
        return 0.0
    return v


def calculate(alpha, g01, g12, g02, g23, g24, g25, g26, d01_grid, d12_grid, d23, d34, d45, d56):
    args = (alpha, alpha, alpha, g01, g12, g02, g23, g24, g25, g26, d01_grid, d12_grid, d23, d34, d45, d56)
    vals = f(*args)
    return snapto0(vals), vals


args = (alpha, g01, g12, g02, g23, g24, g25, g26, d01_grid, d12_grid, d23, d34, d45, d56)
vals, vals_raw = calculate(*args)
val_dict = {"ZZ13": vals_raw}  # to give hover updated values

norm = colors.SymLogNorm(1e-5, vmin=-1e-1, vmax=1e-1)
cmap = OrBu_colormap()

fig, ax, c = make_hoverax_refreshable(d1prim_grid, dd02_grid, val_dict, "ZZ13", norm=norm, cmap=cmap)
ax.set_title("ZZ13")


fig_control = plt.figure()
fig_control.suptitle("Controls")
axslid_g01 = make_axslid(0.06, 0.7, fig_control, 0.35)
axslid_g12 = make_axslid(0.06, 0.6, fig_control, 0.35)
axslid_g02 = make_axslid(0.06, 0.5, fig_control, 0.35)
axslid_g23 = make_axslid(0.06, 0.4, fig_control, 0.35)
axslid_g24 = make_axslid(0.06, 0.3, fig_control, 0.35)
axslid_g25 = make_axslid(0.06, 0.2, fig_control, 0.35)
axslid_g26 = make_axslid(0.06, 0.1, fig_control, 0.35)

axslid_d23 = make_axslid(0.55, 0.4, fig_control, 0.35)
axslid_d34 = make_axslid(0.55, 0.3, fig_control, 0.35)
axslid_d45 = make_axslid(0.55, 0.2, fig_control, 0.35)
axslid_d56 = make_axslid(0.55, 0.1, fig_control, 0.35)

slid_g12 = makeslid(axslid_g01, "g12", 0, 0.01, 0.5, g01)
slid_g23 = makeslid(axslid_g12, "g23", 0, 0.01, 0.5, g12)
slid_g34 = makeslid(axslid_g23, "g34", 0, 0.01, 0.5, g23)
slid_g36 = makeslid(axslid_g25, "g36", 0, 0.01, 0.5, g25)
slid_g13 = makeslid(axslid_g02, "g13", 0, 0.001, 0.1, g02)
slid_g35 = makeslid(axslid_g24, "g35", 0, 0.001, 0.1, g24)
slid_g37 = makeslid(axslid_g26, "g37", 0, 0.001, 0.1, g26)

slids_g = [slid_g12, slid_g23, slid_g13, slid_g34, slid_g35, slid_g36, slid_g37]

slid_d34 = makeslid(axslid_d23, "d34", 0, 0.1, 10, d23)
slid_d45 = makeslid(axslid_d34, "d45", 0, 0.1, 10, d34)
slid_d45 = makeslid(axslid_d45, "d56", 0, 0.1, 10, d45)
slid_d56 = makeslid(axslid_d56, "d67", 0, 0.1, 10, d56)

slids_d = [slid_d34, slid_d45, slid_d45, slid_d56]


def update(val):
    gs = [s.val for s in slids_g]
    ds = [np.float64(s.val) for s in slids_d]

    vals, vals_raw = calculate(alpha, *gs, d01_grid, d12_grid, *ds)
    val_dict["ZZ13"] = vals_raw
    c.set_array(vals)
    fig.canvas.draw_idle()


for s in slids_g + slids_d:
    s.on_changed(update)


plt.show()
