import sympy as sp
import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hamil
from exact.twotransmon.zz.zz import sweep_Eint
from exact.util import omega_alphas, Eint_to_g_Eint, exact_energy

# Sweep ZZ vs Eint

Ej1 = 50
Ej2 = 61
Eints = np.linspace(0, 0.5, 30)
statesperbit = 4
Ham = Hamil(2, statesperbit, "line")
zzexpr: sp.Expr = Ham.getall("11")
swt_zz, vars = Ham.lambdify_expr(zzexpr)
gs = Eint_to_g_Eint(Ej1, Ej2, Eints)
omegas1, alphas1 = omega_alphas(1, Ej1, True)
omega2, alpha2 = omega_alphas(1, Ej2, True)
deltas = omegas1 - omega2

print(vars)

swtvals = swt_zz(alphas1, alpha2, gs, deltas)
exact_zz, exact_zzGS = sweep_Eint(Ej1, Ej2=Ej2, Eints=Eints, k=14)

plt.plot(Eints, swtvals, label="SWT")
plt.plot(Eints, exact_zzGS, label="exact")
plt.title(f"ZZ vs Eint, exact numeric and SWT, Ej1={Ej1}, Ej2={Ej2}")
plt.xlabel("Eint [Ec]")
plt.ylabel("ZZ [Ec]")
plt.legend()
plt.ylim([-4, 4])
plt.show()
