from exact.util import omega_alphas
import numpy as np
from store.stores5T import Store_zz5T_triang
from matplotlib import pyplot as plt
from other.colormap import Norm, OrBu_colormap

Ej1 = np.arange(30, 100, 5)
Ej2 = np.arange(30, 100, 5)
Ej3 = 50
Ej4 = 38
Ej5 = 42

Eint12 = 0.1
Eint23 = 0.1
Eint13 = 0.005
Eint34 = 0.1
Eint45 = 0.1
Eint35 = 0.005
zz13, zz35, zz15, zzz135 = Store_zz5T_triang.plane(
    "Ej2",
    Ej2,
    1,
    "Ej1",
    Ej1,
    1,
    Ej3=Ej3,
    Ej4=Ej4,
    Ej5=Ej5,
    Eint12=Eint12,
    Eint23=Eint23,
    Eint13=Eint13,
    Eint34=Eint34,
    Eint45=Eint45,
    Eint35=Eint35,
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

plt.pcolormesh(o2primgrid, detunegrid, zz13, norm=Norm(1e-1), cmap=OrBu_colormap())
plt.title(
    f"ZZ13 5T triang Ej3={Ej3} Ej4={Ej4} Ej5={Ej5} Eints={Eint12} {Eint23} {Eint13} {Eint34} {Eint45} {Eint35} units [Ec]"
)

plt.xlabel("omega2 prim [Ec]")
plt.ylabel("Detuning [Ec]")
plt.colorbar()


plt.show()
