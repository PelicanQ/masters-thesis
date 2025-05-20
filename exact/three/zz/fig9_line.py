# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap, Norm
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from exact.three.zz.zz import single_zz
from store.stores import Store_zz3T
from exact.util import omega_alphas
from anharm.three.translate import Eints_to_g_Ej

Eints = [0.05, 0.07, 0.09, 0.1]
Ej2 = np.arange(50, 65, 0.2)
for a in Eints:
    zz12, zz23, zz13, zzz = Store_zz3T.meshline(Ej2=Ej2, Ej1=50, Ej3=50, Eint12=a, Eint23=a, Eint13=0, Ec2=1, Ec3=1)
    plt.plot(Ej2, zzz, label=f"zzz {a}")
plt.gca().set_prop_cycle(None)
for a in Eints:
    zz12, zz23, zz13, zzz = Store_zz3T.meshline(Ej2=Ej2, Ej1=50, Ej3=50, Eint12=a, Eint23=a, Eint13=0, Ec2=1, Ec3=1)
    # print(len(zz13))
    plt.plot(Ej2, zz13, label=f"zz13 {a}", linestyle=":")
plt.xlabel("Ej2")
plt.ylabel("Ec")
plt.title("Area of both zero zz13 and zzz. Eint12=Eint23=legend Eint13=0m Ej1=Ej3=50")
plt.legend()
plt.show()
