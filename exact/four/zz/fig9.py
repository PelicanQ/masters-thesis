from exact.util import omega_alphas
import numpy as np
from store.stores4T import Store_zz4T
from matplotlib import pyplot as plt
from other.colormap import Norm, OrBu_colormap
from analysis.discover import make_hoverax

Ej1 = np.arange(30, 100, 1)
Ej2 = np.arange(30, 100, 1)
Ej3 = 50
Ej4 = 56.5

Eint12 = 0.085
Eint23 = 0.085
Eint13 = 0.0046
Eint34 = 0.085

results = Store_zz4T.plane(
    "Ej2",
    Ej2,
    1,
    "Ej1",
    Ej1,
    1,
    Ej3=Ej3,
    Ej4=Ej4,
    Eint12=Eint12,
    Eint23=Eint23,
    Eint13=Eint13,
    Eint34=Eint34,
)


def to_omega_grid(Ej1: np.ndarray, Ej2: np.ndarray, Ej3: float):
    Ej2grid, Ej1grid = np.meshgrid(Ej2, Ej1)
    o3, _ = omega_alphas(1, Ej3, True)
    o1, _ = omega_alphas(1, Ej1grid, True)
    o2, _ = omega_alphas(1, Ej2grid, True)
    o2primgrid = o2 - (o3 + o1) / 2
    detunegrid = o1 - o3
    return o2primgrid, detunegrid


o2primgrid, detunegrid = to_omega_grid(Ej1, Ej2, Ej3)

fig, ax, c = make_hoverax(o2primgrid, detunegrid, results["zzzz"], norm=Norm(1e1), cmap=OrBu_colormap())
ax.set_title(f"ZZ13 4T triang Ej3={Ej3} Ej4={Ej4}  Eints=({Eint12} {Eint23} {Eint13} {Eint34} ) units [Ec]")

ax.set_xlabel("omega2 prim [Ec]")
ax.set_ylabel("Detuning [Ec]")


plt.show()
