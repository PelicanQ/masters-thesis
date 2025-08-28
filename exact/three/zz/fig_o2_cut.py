import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
import initplots


def plot_line():
    E = 0.04
    E13 = 0.0013
    Ej1 = 51
    Ej3 = 50
    Ejs, zz12, zz23, zz13, zzz = Store_zz3T.line(Ec2=1, Ec3=1, Ej1=Ej1, Ej3=Ej3, Eint12=E, Eint23=E, Eint13=E13)
    # Ejs_2, _, _, zz13_2, zzz_2 = Store_zz3T.line(Ec2=1, Ec3=1, Ej1=50, Ej3=50, Eint12=E, Eint23=E, Eint13=E13)
    # plt.rc("lines", marker=".", lw=0, markersize=5)

    o2prim, _ = omega_alphas(1, Ejs, True)
    # o2prim_2, _ = omega_alphas(1, Ejs_2, True)
    plt.figure(figsize=(5.9 * 0.8, 5.9 * 3 / 4 * 0.8), constrained_layout=True)
    plt.rc("lines", markersize=5)
    plt.semilogy(o2prim, np.abs(zz12), label=r"$|\text{ZZ}_{12}|$")
    plt.semilogy(o2prim, np.abs(zz23), label=r"$|\text{ZZ}_{23}|$")
    plt.semilogy(o2prim, np.abs(zz13), label=r"$|\text{ZZ}_{13}|$")
    plt.semilogy(o2prim, np.abs(zzz), label=r"$|\text{ZZZ}|$")
    plt.semilogy(o2prim[::10], np.abs(zz12 + zz23 + zz13)[::10], label="$|\Sigma|$", lw=0, marker=".")
    # plt.title(
    #     f"ZZZ and ZZ for $E_{{J1}}={Ej1}$, $E_{{J3}}={Ej3}$, $E_{{12}}=E_{{23}}={E}$, $E_{{13}}={E13}$ units $E_C$"
    # )
    plt.xlabel("$\omega_2'$ [Ec]")
    plt.ylabel("Magnitude [Ec]")
    plt.ylim([1e-7, 1e0])
    plt.legend()
    plt.savefig("figs/o2-cut.pdf", bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    plot_line()
