import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from numpy.typing import NDArray

thresh = 1e-2  # linearthreshold for symmetric log norm


@np.vectorize
def zzorder2(alpha1, alpha2, g, delta):
    return 2 * g**2 * (-1 / (delta + alpha1) + 1 / (delta - alpha2))


@np.vectorize
def zzorder4(alpha1, alpha2, g, delta):
    simpleedge = 4 * g**4 * (1 / (delta + alpha1) ** 3 - 1 / (delta - alpha2) ** 3)
    edge2 = 4 * g**4 / ((delta + alpha1) * (delta - alpha2)) * (1 / (delta - alpha2) - 1 / (delta + alpha1))
    return simpleedge + edge2


def zz(alpha1, alpha2, g, delta):
    return zzorder2(alpha1, alpha2, g, delta) + zzorder4(alpha1, alpha2, g, delta)


def colormesh():
    # zz vs two variables
    # energy in units of g
    deltas = np.linspace(-4, 4, 800)  # quibit detuning
    alphas = np.linspace(-1, 1, 400)  # alpha1
    alpha2 = -1
    Deltas, Alphas = np.meshgrid(deltas, alphas)
    ZZ2 = zzorder2(Alphas, alpha2, 1, Deltas)
    ZZ4 = zzorder4(Alphas, alpha2, 1, Deltas)
    norm = colors.SymLogNorm(thresh)

    plt.pcolormesh(Deltas, alphas, ZZ2, norm=norm)
    # plt.pcolormesh(Deltas, alphas, ZZ4, norm=norm)

    # plt.title(f"4th order rotating ZZ of 2T, alpha2={alpha2} [g]")
    plt.title(f"2nd order rotating ZZ of 2T, alpha2={alpha2} [g]")

    plt.xlabel("delta [g]")
    plt.ylabel("alpha1 [g]")
    plt.colorbar(label="zz [g]")
    plt.show()


def plotzzdelta():
    # zz vs delta
    deltas = np.linspace(-4, 4, 800)
    # choose units of g
    alpha1 = alpha2 = -1
    term2 = zzorder2(alpha1, alpha2, 1, deltas)
    term4 = zzorder4(alpha1, alpha2, 1, deltas)
    plt.semilogy(deltas, term2, label="2nd order")
    plt.semilogy(deltas, term4, label="4th order")

    plt.semilogy(deltas, term2 + term4, label="sum", linestyle="dotted")

    plt.yscale("symlog", linthresh=thresh)
    plt.ylabel("zz [g]")
    plt.xlabel("delta [g]")
    plt.twinx()

    def levels(delta: NDArray, omega2: float, alpha1: float, alpha2: float):
        omega1 = delta + omega2
        E11 = omega1 + omega2
        E20 = 2 * omega1 + alpha1
        E02 = np.ones(delta.shape) * 2 * omega2 + alpha2
        return E02, E11, E20

    E02, E11, E20 = levels(deltas, omega2=20, alpha1=-0.5, alpha2=-0.5)
    plt.plot(deltas, E11, label="E11", linestyle="--")
    plt.plot(deltas, E02, label="E02", linestyle="--")
    plt.plot(deltas, E20, label="E20", linestyle="--")
    plt.ylabel("E level [g]")
    plt.title("As before, now with bare energies, omega2=20[g]")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # zzdelta()
    colormesh()
