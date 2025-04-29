# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
from analysis.discover import make_hoverax

Ej3 = 50
Ej1s = np.arange(30, 100, 0.5)
Ej2s = np.arange(30, 100, 0.5)
Eint12 = 0.1
Eint23 = 0.1
Eint13 = 0.01
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
print("Fetch done")


def to_omega_grid(Ej1: np.ndarray, Ej2: np.ndarray, Ej3: float):
    Ej2grid, Ej1grid = np.meshgrid(Ej2, Ej1)
    o3, _ = omega_alphas(1, Ej3, True)
    o1, _ = omega_alphas(1, Ej1grid, True)
    o2, _ = omega_alphas(1, Ej2grid, True)
    o2primgrid = o2 - (o3 + o1) / 2
    detunegrid = o1 - o3
    return o2primgrid, detunegrid


o2primgrid, detunegrid = to_omega_grid(Ej1s, Ej2s, Ej3)

fig, ax, c = make_hoverax(o2primgrid, detunegrid, zzz, norm=Norm(1e0), cmap=OrBu_colormap())
ax.set_title(f"ZZZ [Ec] Ej3={Ej3} Eint13={Eint13} Eint12={Eint12} Eint23={Eint23}")

ax.set_xlabel("omega2 prim [Ec]")
ax.set_ylabel("Detuning [Ec]")


plt.show()
