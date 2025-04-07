import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from exact.twotransmon.zz.zz import sweep_Ej1
from exact.util import omega_alphas, Eint_to_g_Ej

# Here we compare exact and swt ZZ while sweeping Ej
Ej2 = 60
Eint = 0.05
statesperbit = 4
Ham = Hamil(2, statesperbit, "line")
zzexpr: sp.Expr = Ham.getall("11")
swt_zz, vars = Ham.lambdify_expr(zzexpr)
Ej1 = np.linspace(30, 90, 150)
gs = Eint_to_g_Ej(Ej1, Ej2, Eint)
omegas1, alphas1 = omega_alphas(1, Ej1, True)
omega2, alpha2 = omega_alphas(1, Ej2, True)
deltas = omegas1 - omega2

print(vars)
swtvals = swt_zz(alphas1, alpha2, gs, deltas)
# exact_zz = np.load("../Ej1sweep60.npy")
exact_zz = sweep_Ej1(Ej1, Ej2=Ej2, Eint=Eint, k=14)
plt.plot(Ej1, swtvals, label="SWT")
plt.plot(Ej1, exact_zz, label="exact")
plt.title(f"ZZ vs Ej1, exact numeric and SWT, Eint={Eint}, Ej2={Ej2}")
plt.xlabel("Ej1 [Ec]")
plt.ylabel("ZZ [Ec]")
# plt.ylim([-2, 3])
plt.legend()
plt.show()
