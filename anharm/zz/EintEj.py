import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from exact.twotransmon.zz.zz import sweep_Eint
from exact.util import omega_alphas

# 2D scan of Ej and Eint
# I think we can find a region of exact zero zz
Ej1s = np.linspace(50, 60, 10)
Ej2 = 50
Eints = np.linspace(0, 0.5, 10)
statesperbit = 4
Ham = Hamil(2, statesperbit, "line")
zzexpr: sp.Expr = Ham.getall("11")
swt_zz, vars = Ham.lambdify_expr(zzexpr)
# gs = Eint_to_g_Eint(Ej1s, Ej2, Eints)
omega1, alpha1 = omega_alphas(1, Ej1s, True)
omega2s, alpha2s = omega_alphas(1, Ej2, True)
deltas = omega1 - omega2s

print(vars)

# swtvals = swt_zz(alpha1, alpha2s, gs, deltas)
data = np.zeros((len(Ej1s), len(Eints)))
for i in range(len(Ej1s)):
    exact_zzs = sweep_Eint(Ej1s[i], Ej2=Ej2, Eints=Eints, k=7)
    data[i, :] = exact_zzs
X, Y = np.meshgrid(Ej1s, Eints)
plt.pcolormesh(X, Y, data)
plt.title(f"ZZ, exact numeric Ej2={Ej2}")
plt.ylabel("Eint [Ec]")
plt.xlabel("Ej1 [Ec]")
plt.colorbar()
plt.show()
