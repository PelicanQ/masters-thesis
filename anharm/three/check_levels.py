import sympy as sp
from sympy import Symbol
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from exact.threetransmon.hamil import eig_excitation_trunc
from anharm.three.translate import Eints_to_g_Ej
from exact.util import omega_alphas
from exact.threetransmon.zz.zz import single_zz


# Compare 3T energies from exact numerics to SWT. This requires translating parameters
## Get exact energies ##
def exact_energies(Ej1s, Ej2, Ej3, Eint12, Eint23, Eint13):
    num_levels = 10
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
        )
        exact_levels[i, :] = vals[:num_levels] - vals[0]
    return exact_levels


## Translate parameters ##


## Get SWT energies##
def sw_energies_1(Ej1: np.ndarray, Ej2, Ej3, Eint12, Eint23, Eint13):
    keep = False
    omega1, alpha1 = omega_alphas(1, Ej1, True)
    omega2, alpha2 = omega_alphas(1, Ej2, True)
    omega3, alpha3 = omega_alphas(1, Ej3, True)
    g12, g23, g13 = Eints_to_g_Ej(Ej1, Ej2, Ej3, Eint12, Eint23, Eint13)
    # print(g12, g23, g13)
    Ham = Hamil(3, 4, "line")

    e001: sp.Expr = Ham.split_deltas(Ham.getall("001", keep_second_coupling=keep))
    e010: sp.Expr = Ham.split_deltas(Ham.getall("010", keep_second_coupling=keep))
    e100: sp.Expr = Ham.split_deltas(Ham.getall("100", keep_second_coupling=keep))

    f100, var100 = Ham.lambdify_expr(e100)
    f010, var010 = Ham.lambdify_expr(e010)
    f001, var001 = Ham.lambdify_expr(e001)  #

    delta12 = omega1 - omega2
    delta23 = np.ones(omega1.shape) * (omega2 - omega3)
    E100 = f100(g12, g23, delta12, delta23) + omega1
    E010 = f010(g12, g23, delta12, delta23) + omega2
    E001 = f001(g12, g23, delta12, delta23) + omega3

    return E001, E010, E100


def sw_energies_2(Ej1: np.ndarray, Ej2, Ej3, Eint12, Eint23, Eint13):
    keep = False
    omega0, alpha0 = omega_alphas(1, Ej1, True)
    omega1, alpha1 = omega_alphas(1, Ej2, True)
    omega2, alpha2 = omega_alphas(1, Ej3, True)
    g12, g23, g13 = Eints_to_g_Ej(Ej1, Ej2, Ej3, Eint12, Eint23, Eint13)
    # print(g12, g23, g13)
    Ham = Hamil(3, 4, "line")

    e002: sp.Expr = Ham.split_deltas(Ham.getall("002", keep_second_coupling=keep))
    e020: sp.Expr = Ham.split_deltas(Ham.getall("020", keep_second_coupling=keep))
    e200: sp.Expr = Ham.split_deltas(Ham.getall("200", keep_second_coupling=keep))

    e110: sp.Expr = Ham.split_deltas(Ham.getall("110", keep_second_coupling=keep))
    e101: sp.Expr = Ham.split_deltas(Ham.getall("101", keep_second_coupling=keep))
    e011: sp.Expr = Ham.split_deltas(Ham.getall("011", keep_second_coupling=keep))

    f200, var200 = Ham.lambdify_expr(e200)
    f020, var020 = Ham.lambdify_expr(e020)
    f002, var002 = Ham.lambdify_expr(e002)  # alpha0 alpha1 alpha2 g12 g23 g13 d12 d23

    f110, var110 = Ham.lambdify_expr(e110)
    f101, var101 = Ham.lambdify_expr(e101)
    f011, var011 = Ham.lambdify_expr(e011)  # alpha0 alpha1 alpha2 g12 g23 g13 d12 d23

    print(var002, var020, var200, var110, var101, var011)
    delta12 = omega0 - omega1
    delta23 = np.ones(omega0.shape) * (omega1 - omega2)

    E200 = f200(alpha0, alpha1, g12, g23, delta12, delta23) + 2 * omega0 + alpha0
    E020 = f020(alpha0, alpha1, alpha2, g12, g23, delta12, delta23) + 2 * omega1 + alpha1
    E002 = f002(alpha1, alpha2, g12, g23, delta12, delta23) + 2 * omega2 + alpha2

    E110 = f110(alpha0, alpha1, g12, g23, delta12, delta23) + omega0 + omega1
    E101 = f101(alpha0, alpha1, alpha2, g12, g23, delta12, delta23) + omega0 + omega2
    E011 = f011(alpha1, alpha2, g12, g23, delta12, delta23) + omega1 + omega2
    return E200, E020, E002, E110, E101, E011


if __name__ == "__main__":
    Ej1s = np.linspace(30, 80, 200)
    Ej1s_small = np.linspace(30, 80, 50)
    Ej2 = 53
    Ej3 = 50
    Eint12 = 0.05
    Eint23 = 0.05
    Eint13 = 0

    o0, alpha0 = omega_alphas(1, Ej1s_small, True)
    o1, alpha1 = omega_alphas(1, Ej2, True)
    o2, alpha2 = omega_alphas(1, Ej3, True)
    # exact_levels = exact_energies(Ej1s_small, Ej2, Ej3, Eint12, Eint23, Eint13)

    sw001, sw010, sw100 = sw_energies_1(Ej1s, Ej2, Ej3, Eint12, Eint23, Eint13)
    sw200, sw020, sw002, sw110, sw101, sw011 = sw_energies_2(Ej1s, Ej2, Ej3, Eint12, Eint23, Eint13)
    #
    #
    #### PLOT
    # plt.plot(Ej1s_small, exact_levels, linestyle=":", color="gray")
    plt.gca().set_prop_cycle(None)

    # SWT
    # plt.plot(Ej1s, sw001, label="001 SW")
    # plt.plot(Ej1s, sw010, label="010 SW")
    # plt.plot(Ej1s, sw100, label="100 SW")
    # plt.plot(Ej1s, sw002, label="002 SW")
    # plt.plot(Ej1s, sw020, label="020 SW")
    # plt.plot(Ej1s, sw200, label="200 SW")
    # plt.plot(Ej1s, sw110, label="110 SW")
    # plt.plot(Ej1s, sw101, label="101 SW")
    # plt.plot(Ej1s, sw011, label="011 SW")
    # plt.plot(Ej1s, sw111, label="111 SW")
    v = []
    for Ej1 in Ej1s_small:
        zz12, zz23, zz13, zzz = single_zz(1, 1, Ej1, Ej2, Ej3, Eint12, Eint23, 0)
        v.append(zz23)
    zz23 = sw011 - sw001 - sw010
    # zzexact = exact_levels[:, 6] - exact_levels[:, 1] - exact_levels[:, 2]
    plt.plot(Ej1s, zz23)
    plt.plot(Ej1s_small, v)
    # Bare
    ones = np.ones(o0.shape)
    bares = [
        o0,
        o1,
        o2,
        2 * o0 + alpha0,
        2 * o1 + alpha1,
        2 * o2 + alpha2,
        o0 + o1,
        o1 + o2,
        o0 + o2,
    ]
    bares = [ones * b for b in bares]
    # for b in bares:
    #     plt.plot(Ej1s_small, b, lw=0, marker=".")

    # plt.title(f"Comparison between SWT and exact energies in 2T. Eint={Eint}, Ej2={Ej2}")

    plt.xlabel("Ej1 [Ec]")
    plt.ylabel("En - E0 [Ec]")
    plt.legend()
    plt.ylim([-10, 90])
    plt.show()
