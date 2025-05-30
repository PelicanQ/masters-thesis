from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
from matplotlib import colors

Ej3 = 50
Ej1s = np.arange(30, 100, 1)
Ej2s = np.arange(30, 140, 1)
Eint12 = 0.04
Eint23 = 0.04
Eint13 = 0.0013
_, _, _, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)


def to_omega_grid(Ej1: np.ndarray, Ej2: np.ndarray, Ej3: float):
    Ej2grid, Ej1grid = np.meshgrid(Ej2, Ej1)
    o3, _ = omega_alphas(1, Ej3, True)
    o1, _ = omega_alphas(1, Ej1grid, True)
    o2, _ = omega_alphas(1, Ej2grid, True)
    o2primgrid = o2 - (o3 + o1) / 2
    detunegrid = o1 - o3
    return o2primgrid, detunegrid


o2primgrid, detunegrid = to_omega_grid(Ej1s, Ej2s, Ej3)
plt.pcolormesh(o2primgrid, detunegrid, zzz, norm=Norm(1e-0), cmap=OrBu_colormap())

# m = np.zeros_like(o2primgrid)
# for i in range(o2primgrid.shape[0]):
#     for j in range(o2primgrid.shape[1]):
#         o2prim = o2primgrid[i,j]
#         if
#             m=1
plt.pcolormesh(o2primgrid, detunegrid, zzz, norm=Norm(1e-0), cmap=OrBu_colormap())

plt.title(rf"ZZZ Ej3={Ej3}  Eint12={Eint12} Eint23={Eint23} Eint13={Eint13} units [Ec]")
plt.xlabel("$\omega_2^\prime$ [Ec]")
plt.ylabel("$\Delta_{13}$ [Ec]")
plt.xlim([-6, 14])
plt.colorbar()
plt.show()
