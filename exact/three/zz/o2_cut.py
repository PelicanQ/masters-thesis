import numpy as np
from matplotlib import pyplot as plt
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
import scienceplots


def plot_line():
    E = 0.04
    E13 = 0.008
    Ej1 = 50
    Ejs, zz12, zz23, zz13, zzz = Store_zz3T.line(Ec2=1, Ec3=1, Ej1=Ej1, Ej3=50, Eint12=E, Eint23=E, Eint13=E13)
    # Ejs_2, _, _, zz13_2, zzz_2 = Store_zz3T.line(Ec2=1, Ec3=1, Ej1=50, Ej3=50, Eint12=E, Eint23=E, Eint13=E13)
    # plt.rc("lines", marker=".", lw=0, markersize=5)

    o2prim, _ = omega_alphas(1, Ejs, True)
    # o2prim_2, _ = omega_alphas(1, Ejs_2, True)
    plt.figure(figsize=(1, 1))
    plt.rc("lines", markersize=5)
    # plt.semilogy(o2prim, np.abs(zz12), label="zz12")
    # plt.semilogy(o2prim, np.abs(zz23), label="zz23")
    plt.semilogy(o2prim, np.abs(zz13), label="zz13")
    plt.semilogy(o2prim, np.abs(zzz), label="zzz")
    # plt.semilogy(o2prim[::3], np.abs(zz12 + zz23 + zz13)[::3], label="sum", lw=0, marker=".")
    plt.gca().set_prop_cycle(None)

    plt.title(f"Magnitude of ZZZ and ZZ's Ej1={Ej1} Ej3=50 E12=E23={E} E13={E13}. Units Ec")
    plt.xlabel("omega2 [Ec]")
    plt.ylabel("Magnitude [Ec]")
    plt.legend()
    plt.savefig("figs/o2-cut.png", dpi=300, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    plot_line()
