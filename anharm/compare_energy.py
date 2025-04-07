import sympy as sp
from sympy import Symbol
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from anharm.Subspace import Hamil
from exact.twotransmon.hamil import eig_clever
from exact.util import omega_alphas, Eint_to_g_Ej

# Compare 2T energies from exact numerics to SWT. This requires translating parameters
Ej1 = np.linspace(0, 90, 100)
Ej2 = 50
Eint = 0.5
omega1s, alpha1s = omega_alphas(1, Ej1, True)
omega2, alpha2 = omega_alphas(1, Ej2, True)
gs = Eint_to_g_Ej(Ej1, Ej2, Eint)
Ham = Hamil(2, 3, "line")
e0: sp.Expr = Ham.getall("00")
e1: sp.Expr = Ham.getall("10")
e2: sp.Expr = Ham.getall("01")
e3: sp.Expr = Ham.getall("11")
e20: sp.Expr = Ham.getall("20")
e02: sp.Expr = Ham.getall("02")
ex0, vars0 = Ham.lambdify_expr(e0)
ex1, vars1 = Ham.lambdify_expr(e1)
ex2, vars2 = Ham.lambdify_expr(e2)
ex3, vars3 = Ham.lambdify_expr(e3)
ex20, vars20 = Ham.lambdify_expr(e20)
ex02, vars02 = Ham.lambdify_expr(e02)
deltas = omega1s - omega2
E0 = 0
E1 = ex1(gs, deltas) + omega1s
E2 = ex2(gs, deltas) + omega2
E3 = ex3(alpha1s, alpha2, gs, deltas) + omega1s + omega2
E20 = ex20(alpha1s, alpha2, gs, deltas) + 2 * omega1s + alpha1s
E02 = ex02(alpha1s, alpha2, gs, deltas) + 2 * omega2 + alpha2
print(vars0, vars1, vars2, vars3, vars20, vars02)
num_levels = 6

exact_levels = np.zeros((len(Ej1), num_levels))
for i, Ej in enumerate(Ej1):
    vals = eig_clever(Ej1=Ej, Ej2=Ej2, Eint=Eint, ng1=0, k=15, only_energy=True)
    exact_levels[i, :] = vals[:num_levels] - vals[0]

# Exact
plt.plot(Ej1, exact_levels[:, 3:], lw=0, marker="x")
plt.gca().set_prop_cycle(None)
# SWT
# plt.plot(Ej1, E1, label="10 SWT")
# plt.plot(Ej1, E2, label="01 SWT")
plt.plot(Ej1, E3, label="11 SWT")
plt.plot(Ej1, E20, label="20 SWT")
plt.plot(Ej1, E02, label="02 SWT")
# Bare
plt.gca().set_prop_cycle(None)
# plt.plot(Ej1, omega1s, lw=0, marker=".", label="10")
plt.plot(Ej1, 2 * omega1s + alpha1s, lw=0, marker=".", label="20")
# plt.plot(Ej1, omega2 * np.ones_like(omega1s), lw=0, marker=".", label="01")
plt.plot(Ej1, (2 * omega2 + alpha2) * np.ones_like(omega1s), lw=0, marker=".", label="02")
plt.plot(Ej1, omega1s + omega2, lw=0, marker=".", label="11")

plt.gca().set_prop_cycle(None)
plt.title(
    f"Comparison between SWT and exact energies in 2T. X=exact numeric, dots=bare translated, line=SWT, Eint={Eint}, Ej2={Ej2}"
)
plt.xlabel("Ej1 [Ec]")
plt.ylabel("En - E0 [Ec]")
plt.legend()
plt.ylim([-10, 90])
plt.show()
