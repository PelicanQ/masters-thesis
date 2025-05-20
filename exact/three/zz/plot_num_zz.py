# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import to_omega_grid
from analysis.discover import make_hoverax
from matplotlib import colors

Ej3 = 50
Ej1s = np.arange(30, 100, 1)
Ej2s = np.arange(30, 140, 1)
# Ej1s = np.arange(45, 60, 1)
# Ej2s = np.arange(60, 100, 1)
Eint12 = 0.04
Eint23 = 0.04
Eint13 = 0.0013
zz12, zz23, zz13, _ = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)


o2primgrid, detunegrid = to_omega_grid(Ej1s, Ej2s, Ej3)
# a = 10
# b = 71
# print(zzz[a, b], zz13[a, b])
# print(o2primgrid[a, b], detunegrid[a, b])
# f = np.abs(zzz - (zz12 + zz23 + zz13)) / np.abs(zzz)
# fig, ax, c = make_hoverax(o2primgrid, detunegrid, zzz, norm=Norm(1e0), cmap=OrBu_colormap())
fig, ax, c, cbar = make_hoverax(Ej2s, Ej1s, zz13, norm=Norm(1e-2), cmap=OrBu_colormap())
# ax.set_xlim(-6, 14)
ax.set_title(rf"ZZ13 Ej3={Ej3}  Eint12={Eint12} Eint23={Eint23} Eint13={Eint13} units [Ec]")
ax.set_xlabel("$\omega_2^\prime$ [Ec]")
ax.set_ylabel("$\Delta_{13}$ [Ec]")

plt.show()
