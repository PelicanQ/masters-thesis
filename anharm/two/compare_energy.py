import sympy as sp
from sympy import Symbol
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from exact.twotransmon.hamil import eig_clever
from exact.util import omega_alphas
from anharm.two.translate import Eint_to_g_Ej


# Compare 2T energies from exact numerics to SWT. This requires translating parameters
## Get exact energies ##
def exact_energies(Ej1s, Ej2: float, Eint: float):
    num_levels = 6
    exact_levels = np.zeros((len(Ej1s), num_levels))
    for i, Ej in enumerate(Ej1s):
        vals = eig_clever(Ej1=Ej, Ej2=Ej2, Eint=Eint, only_energy=True)
        exact_levels[i, :] = vals[:num_levels] - vals[0]
    return exact_levels


## Translate parameters ##


## Get SWT energies##
def sw_energies(Ej1: np.ndarray, Ej2: float, Eint):
    keep = False
    omega1s, alpha1s = omega_alphas(1, Ej1, True)
    omega2, alpha2 = omega_alphas(1, Ej2, True)
    gs = Eint_to_g_Ej(Ej1, Ej2, Eint)
    Ham = Hamil(2, 3, "line")
    e10: sp.Expr = Ham.getall("10", keep_second_coupling=keep)
    e01: sp.Expr = Ham.getall("01", keep_second_coupling=keep)
    e11: sp.Expr = Ham.getall("11", keep_second_coupling=keep)
    e20: sp.Expr = Ham.getall("20", keep_second_coupling=keep)
    e02: sp.Expr = Ham.getall("02", keep_second_coupling=keep)
    f01, vars01 = Ham.lambdify_expr(e01)
    f10, vars10 = Ham.lambdify_expr(e10)
    f11, vars11 = Ham.lambdify_expr(e11)
    f20, vars20 = Ham.lambdify_expr(e20)
    f02, vars02 = Ham.lambdify_expr(e02)
    print(vars01, vars10, vars11, vars20, vars02)
    deltas = omega1s - omega2
    E0 = 0
    E01 = f01(gs, deltas) + omega2
    E10 = f10(gs, deltas) + omega1s
    E11 = f11(alpha1s, alpha2, gs, deltas) + omega1s + omega2
    E20 = f20(alpha1s, alpha2, gs, deltas) + 2 * omega1s + alpha1s
    E02 = f02(alpha1s, alpha2, gs, deltas) + 2 * omega2 + alpha2
    return E01, E10, E11, E02, E20


Ej1s = np.linspace(30, 90, 200)
Ej2 = 50
Eint = 0.2
exact_levels = exact_energies(Ej1s, Ej2, Eint)
sw01, sw10, sw11, sw02, sw20 = sw_energies(Ej1s, Ej2, Eint)
##  PLOT ###

# Exact
plt.plot(Ej1s, exact_levels, linestyle=":", color="gray")
plt.gca().set_prop_cycle(None)

# SWT
plt.plot(Ej1s, sw01, label="01 SW")
plt.plot(Ej1s, sw10, label="10 SW")
plt.plot(Ej1s, sw11, label="11 SWT")
plt.plot(Ej1s, sw02, label="02 SWT")
plt.plot(Ej1s, sw20, label="20 SWT")

# Bare
# plt.gca().set_prop_cycle(None)
# plt.plot(Ej1, omega1s, lw=0, marker=".", label="10")
# plt.plot(Ej1, 2 * omega1s + alpha1s, lw=0, marker=".", label="20")
# plt.plot(Ej1, omega2 * np.ones_like(omega1s), lw=0, marker=".", label="01")
# plt.plot(Ej1, (2 * omega2 + alpha2) * np.ones_like(omega1s), lw=0, marker=".", label="02")
# plt.plot(Ej1, omega1s + omega2, lw=0, marker=".", label="11")

plt.gca().set_prop_cycle(None)
plt.title(f"Comparison between SWT and exact energies in 2T. Eint={Eint}, Ej2={Ej2}")
plt.xlabel("Ej1 [Ec]")
plt.ylabel("En - E0 [Ec]")
plt.legend()
plt.ylim([-10, 90])
plt.show()
