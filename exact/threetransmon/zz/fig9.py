# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from exact.threetransmon.zz.zz import single_zz
from store.stores import Store_zz3T
from exact.util import omega_alphas

Ej3 = 50
Ej1s = np.arange(30, 80, 0.2)
Ej2s = np.arange(30, 80, 0.2)
Eint12 = 0.1
Eint23 = 0.1
Eint13 = 0
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, "Ej1", Ej1s, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
print("Fetch done")
# o1, _ = omega_alphas(1, Ej1s, True)
# o2, _ = omega_alphas(1, Ej2s, True)
o3, _ = omega_alphas(1, Ej3, True)
# o2prim = o2 - (o1 + o3) / 2
# detun = o1 - o3

Ej2grid, Ej1grid = np.meshgrid(Ej2s, Ej1s)
o2primgrid = np.zeros_like(Ej1grid, dtype=float)
detunegrid = np.zeros_like(Ej1grid, dtype=float)
for i in range(len(Ej1s)):
    for j in range(len(Ej2s)):
        o1, _ = omega_alphas(1, Ej1grid[i, j], True)
        o2, _ = omega_alphas(1, Ej2grid[i, j], True)
        print(o1, o2, o3)
        o2prim = o2 - (o3 + o1) / 2
        detun = o1 - o3
        o2primgrid[i, j] = o2prim
        detunegrid[i, j] = detun
# o1, _ = omega_alphas(1, Ej1s, True)
# o2, _ = omega_alphas(1, Ej2s, True)
plt.pcolormesh(o2primgrid, detunegrid, zzz, norm=Norm(1e1), cmap=OrBu_colormap())
plt.title("ZZZ [Ec] Ej3=50 Eint13=0 Eint12=Eint23=0.1")
plt.xlabel("omega2 prim [Ec]")
plt.ylabel("Detuning [Ec]")
plt.colorbar()
# plt.figure()
# vars, zz12, zz23, zz13, zzz = Store_zz3T.line(
#     Ej1=70, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
# )

# plt.plot(vars, zz13)

plt.show()
