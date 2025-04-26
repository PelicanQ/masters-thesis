from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from jobmanager.util import collect_jobs
from anharm.Hamiltonian import Hamil
from matplotlib import colors
from store.stores import Store_zz3T
from exact.util import omega_alphas
from anharm.three.translate import Eints_to_g_Ej

Ej2 = 53
Ej3 = 50
Eint = 0.05
# Let's check that the zzz from SWT stays true to numerics
Ej1, zz12, zz23, zz13, zzz = Store_zz3T.line(Ej2=Ej2, Ej3=Ej3, Ec2=1, Ec3=1, Eint12=Eint, Eint23=Eint, Eint13=0)

o0, alpha0 = omega_alphas(1, Ej1, True)
o1, alpha1 = omega_alphas(1, Ej2, True)
o2, alpha2 = omega_alphas(1, Ej3, True)
g01, g12, g02 = Eints_to_g_Ej(Ej1, Ej2, Ej3, Eint, Eint, 0)

H = Hamil(3, 4, "line")
e = (
    H.get_all("011", True)
    - H.get_second_edges("011", True)
    - H.get_all("010", True)
    - H.get_all("001", True)
    + H.get_second_edges("001", True)
)
e = H.zzexpr("011", type="edges") + H.zzexpr("011", type="birds") + H.zzexpr("011", type="4loop")
e = H.zzexpr("011")
e = H.split_deltas(e)
f, f_vars = H.lambdify_expr(e)
print("vars", f_vars)
d01 = o0 - o1
d12 = o1 - o2


vals = f(alpha1, alpha2, g01, g12, d01, d12)
plt.plot(Ej1, zz23)
plt.plot(Ej1, vals)
# plt.title("ZZZ [alpha] g12=g23=0.3 g13=g12/30")
# plt.ylabel("delta13")
plt.xlabel("Ej1")
# plt.ylim([-0.04, 0.04])
# plt.colorbar()
plt.show()
