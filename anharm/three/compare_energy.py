import sympy as sp
from sympy import Symbol
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from exact.threetransmon.hamil import eig_excitation_trunc
from anharm.three.translate import Eints_to_g_Ej
from exact.util import omega_alphas


# Compare 3T energies from exact numerics to SWT. This requires translating parameters
## Get exact energies ##
def exact_energies(Ej1s, Ej2, Ej3, Eint12, Eint23, Eint13):
    num_levels = 4
    exact_levels = np.zeros((len(Ej1s), num_levels))
    for i, Ej in enumerate(Ej1s):
        vals = eig_excitation_trunc(
            Ec2=1,
            Ec3=1,
            Ej1=Ej,
            Ej2=Ej2,
            Ej3=Ej3,
            Eint12=Eint12,
            Eint23=Eint23,
            Eint13=Eint13,
            only_energy=True,
            k=7,
            M=25,
        )
        exact_levels[i, :] = vals[:num_levels] - vals[0]
    return exact_levels


## Translate parameters ##


## Get SWT energies##
def sw_energies(Ej1: np.ndarray, Ej2, Ej3, Eint12, Eint23, Eint13):
    keep = False
    omega1s, alpha1s = omega_alphas(1, Ej1, True)
    omega2, alpha2 = omega_alphas(1, Ej2, True)
    omega3, alpha3 = omega_alphas(1, Ej3, True)
    g12, g23, g13 = Eints_to_g_Ej(Ej1, Ej2, Ej3, Eint12, Eint23, Eint13)
    Ham = Hamil(3, 3, "triang")

    e001: sp.Expr = Ham.split_deltas(Ham.getall("001", keep_second_coupling=keep))
    e010: sp.Expr = Ham.split_deltas(Ham.getall("010", keep_second_coupling=keep))
    e100: sp.Expr = Ham.split_deltas(Ham.getall("100", keep_second_coupling=keep))

    f001, var001 = Ham.lambdify_expr(e001)
    f010, var010 = Ham.lambdify_expr(e010)
    f100, var100 = Ham.lambdify_expr(e100)

    print(var001, var010, var100)
    delta12 = omega1s - omega2
    delta23 = np.ones_like(omega1s) * (omega2 - omega3)
    print(g12, g23, g13, delta12, delta23)
    E001 = f001(g12, g23, g13, delta12, delta23) + omega1s
    E010 = f010(g12, g23, g13, delta12, delta23) + omega2
    E100 = f100(g12, g23, g13, delta12, delta23) + omega3
    return E001, E010, E100


if __name__ == "__main__":
    Ej1s = np.linspace(30, 80, 200)
    Ej1s_small = np.linspace(30, 80, 40)
    Ej2 = 50
    Ej3 = 60
    Eint12 = 0.2
    Eint23 = 0.1
    Eint13 = 0.1

    o1, _ = omega_alphas(1, Ej1s_small, True)
    o2, _ = omega_alphas(1, Ej2, True)
    o3, _ = omega_alphas(1, Ej3, True)
    exact_levels = exact_energies(Ej1s_small, Ej2, Ej3, Eint12, Eint23, Eint13)
    sw001, sw010, sw100 = sw_energies(Ej1s, Ej2, Ej3, Eint12, Eint23, Eint13)
    #
    #
    #### PLOT
    plt.plot(Ej1s_small, exact_levels, linestyle=":", color="gray")
    plt.gca().set_prop_cycle(None)

    # SWT
    plt.plot(Ej1s, sw001, label="001 SW")
    plt.plot(Ej1s, sw010, label="010 SW")
    plt.plot(Ej1s, sw100, label="100 SW")

    # Bare
    plt.plot(Ej1s_small, o1, lw=0, marker=".")
    plt.plot(Ej1s_small, np.ones_like(o1) * o2, lw=0, marker=".")
    plt.plot(Ej1s_small, np.ones_like(o1) * o3, lw=0, marker=".")
    # plt.title(f"Comparison between SWT and exact energies in 2T. Eint={Eint}, Ej2={Ej2}")

    plt.xlabel("Ej1 [Ec]")
    plt.ylabel("En - E0 [Ec]")
    plt.legend()
    plt.ylim([-10, 90])
    plt.show()
