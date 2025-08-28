import numpy as np
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
from matplotlib import pyplot as plt, colors
from other.colormap import OrBu_colormap, Norm
import initplots


Ej3 = 50
Ej1s = np.arange(30, 100, 0.2)
Ej2s = np.arange(30, 140, 0.2)

Eint12 = 0.04
Eint23 = 0.04
Eint13 = 0.0013
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
zz12_flat = zz12.flatten()
zz23_flat = zz23.flatten()
zz13_flat = zz13.flatten()
zzz_flat = zzz.flatten()


Ej2grid, Ej1grid = np.meshgrid(Ej2s, Ej1s)
o3, _ = omega_alphas(1, Ej3, True)
o1, _ = omega_alphas(1, Ej1grid, True)
o2, _ = omega_alphas(1, Ej2grid, True)
o2primgrid = o2 - (o3 + o1) / 2
detunegrid = o1 - o3


alpha = 1.25


def linear_reg(zz12_vec, zz23_vec, zz13_vec, zzz_vec):
    # one = np.ones_like(zzz_vec)
    # recreate figure 6 in ZZ paper

    A = np.column_stack([zz12_vec, zz23_vec, zz13_vec])
    print(f"Num {A.shape[0]}", end="")

    x, ssr, rank, s = np.linalg.lstsq(A, zzz_vec)
    print(" Coeff", x, end="")

    sst = np.sum((zzz_vec - np.mean(zzz_vec)) ** 2)  # Total sum of squares
    r_squared = 1 - (ssr / sst)
    print(" R2", r_squared)
    return x


def region():
    global left, right
    right = np.zeros_like(o2primgrid)
    left = np.zeros_like(o2primgrid)
    band = np.zeros_like(o2primgrid)
    regi = np.zeros_like(o2primgrid)

    for i in range(o2primgrid.shape[0]):
        for j in range(o2primgrid.shape[1]):
            o2prim = o2primgrid[i, j]
            d13 = detunegrid[i, j]
            o1 = 0
            o2 = -d13 / 2 + o2prim
            o3 = -d13
            if o2prim > abs(d13) / 2 + 1.5 * alpha:
                regi[i, j] = 1
                right[i, j] = 1
            # if o2 < o1 - alpha * 1.5:
            #     regi[i, j] = 2
            #     left[i, j] = 1
            # if abs(o2prim) < abs(d13) / 2 - 1.2 * alpha and d13 > 0:
            #     left[i, j] = 1
            #     regi[i, j] = 2
            # if abs(d13) < alpha * 0.9 and o2prim > 2 * alpha:
            # band up-left
            # band[i, j] = 1

    def perone(mask):
        sel12 = []
        sel23 = []
        sel13 = []
        selzzz = []

        for i in range(o2primgrid.shape[0]):
            for j in range(o2primgrid.shape[1]):
                if mask[i, j]:
                    sel12.append(zz12[i, j])
                    sel23.append(zz23[i, j])
                    sel13.append(zz13[i, j])
                    selzzz.append(zzz[i, j])
        sel12 = np.array(sel12)
        sel23 = np.array(sel23)
        sel13 = np.array(sel13)
        selzzz = np.array(selzzz)
        linear_reg(sel12, sel23, sel13, selzzz)

    print("right")
    perone(right)
    print("left")
    perone(left)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, sharex=True, sharey=True, constrained_layout=True, figsize=(5.9 * 0.8, 5.9 * 3 / 4 * 0.8)
    )
    plt.xlim([-6, 14])
    plt.ylim([-4, 8])
    ax1.pcolormesh(o2primgrid, detunegrid, regi, rasterized=True)
    a = 2 * alpha
    ax1.plot(o2primgrid, 2 * o2primgrid - a)
    ax1.plot(o2primgrid, 2 * o2primgrid + a)
    ax1.plot(o2primgrid, -2 * o2primgrid + a)
    ax1.plot(o2primgrid, -2 * o2primgrid - a)

    ax2.pcolormesh(o2primgrid, detunegrid, zzz, norm=Norm(1), cmap=OrBu_colormap(), rasterized=True)
    ax2.plot(o2primgrid, 2 * o2primgrid - a)
    ax2.plot(o2primgrid, 2 * o2primgrid + a)
    ax2.plot(o2primgrid, -2 * o2primgrid + a)
    ax2.plot(o2primgrid, -2 * o2primgrid - a)

    ax1.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
    ax2.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
    ax2.set_xlabel(r"$\omega_2'$ [$E_C$]")
    fig.savefig("figs/regions.pdf", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    region()
    # linear(zz12_flat, zz23_flat, zz13_flat, zzz_flat)
    pass
