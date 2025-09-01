from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
from matplotlib import pyplot as plt, colors

# Here we plot how well ZZs predict ZZZ

Ej3 = 50
Ej1s = np.arange(30, 100, 1)
Ej2s = np.arange(30, 140, 1)

Eint12 = 0.04
Eint23 = 0.04
Eint13 = 0.0013
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
# vars, zz12, zz23, zz13, zzz = Store_zz3T.line(
#     Ej2=60, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
# )
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


@np.vectorize
def fn(x):
    return np.arcsinh(x * 1e2)


@np.vectorize
def invfn(x):
    return np.sinh(x) * 1e-2


def linear_func(zz12_vec, zz23_vec, zz13_vec, zzz_vec):
    ssr = np.sum(np.square(zzz_vec - (zz12_vec + zz23_vec + zz13_vec)))
    sst = np.sum((zzz_vec - np.mean(zzz_vec)) ** 2)  # Total sum of squares
    r_squared = 1 - (ssr / sst)
    print(" R2", r_squared)


def linear(zz12_vec, zz23_vec, zz13_vec, zzz_vec):
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


def predict():
    b12 = 1.07120666
    b23 = 0.96583636
    b13 = 0.24216915
    pred_big = b12 * zz12 + b23 * zz23 + b13 * zz13
    rel = np.abs(zzz - pred_big) / np.abs(zzz)
    plt.pcolormesh(o2primgrid, detunegrid, rel, vmin=0.01, vmax=0.1)
    plt.colorbar()
    plt.title(f"rel error of upper region fit sum, E12=E23={Eint12} E13={Eint13}")
    plt.xlabel(r"$\omega_2'$")
    plt.ylabel(r"$\Delta_{13}$")
    plt.xlim([-6, 14])
    plt.show()


alpha = 1.25


def predict_fig():
    # arcsinh big
    a12 = 1.00314978  # 0.99501465
    a23 = 1.06638546
    a13 = 4.09027235

    b12 = 1.07120666  # [0.95486379]
    b23 = 0.96583636
    b13 = 0.24216915

    pred111 = zz12 + zz23 + zz13
    preda = a12 * zz12 + a23 * zz23 + a13 * zz13
    predb = b12 * zz12 + b23 * zz23 + b13 * zz13
    rel111 = np.abs(zzz - pred111) / np.abs(zzz)
    rela = np.abs(zzz - preda) / np.abs(zzz)
    relb = np.abs(zzz - predb) / np.abs(zzz)

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True, constrained_layout=True, figsize=(10, 5))

    colorss = plt.cm.Oranges(np.linspace(0, 0.8, 20))
    # Finally, create a continuous map from the discrete one
    cmap = colors.LinearSegmentedColormap.from_list("my_colormap", colorss)
    for x in np.arange(-20, 20, 1):
        ax1.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)
        ax2.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)
    # ax2.axline(x=xg, color="gray", linestyle="-", linewidth=0.5, zorder=0)

    c = ax1.pcolormesh(o2primgrid, detunegrid, rel111, vmin=0.01, vmax=0.1, cmap=cmap, zorder=1)
    ax2.pcolormesh(o2primgrid, detunegrid, rela, vmin=0.01, vmax=0.1, cmap=cmap)
    xx = o2primgrid[0, :30]

    xx1 = o2primgrid[0, 20:40]
    xx2 = o2primgrid[0, 10:40]
    # ax2.plot(xx, xx / xx * 1.25, color="red")
    # ax1.plot(xx1, 2 * (xx1 - 1.25), color="red")
    ax1.set_title(f"rel error of upper region fit sum, E12=E23={Eint12} E13={Eint13}")
    ax1.set_xlabel(r"$\omega_2'$ [$E_C$]")
    ax1.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
    ax1.set_ylim([-4, 8])
    ax1.set_xlim([-6, 14])

    ax2.set_xlabel(r"$\omega_2'$ [$E_C$]")

    # cbar = fig.colorbar(c, ax=[ax1, ax2])
    # cbar.set_ticks(np.arange(0.01, 0.11, 0.01))

    plt.show()


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
            if o2 < o1 - alpha * 1.5:
                regi[i, j] = 2
                left[i, j] = 1
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
        linear(sel12, sel23, sel13, selzzz)

    print("right")
    perone(right)
    print("left")
    perone(left)

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True, constrained_layout=True, figsize=(10, 5))
    plt.xlim([-9, 16])
    plt.ylim([-5, 8.5])
    ax1.pcolormesh(o2primgrid, detunegrid, regi)
    a = 2 * 1.25
    ax1.plot(o2primgrid, 2 * o2primgrid - a)
    ax1.plot(o2primgrid, 2 * o2primgrid + a)
    ax1.plot(o2primgrid, -2 * o2primgrid + a)
    ax1.plot(o2primgrid, -2 * o2primgrid - a)

    ax2.pcolormesh(o2primgrid, detunegrid, zzz)
    ax2.plot(o2primgrid, 2 * o2primgrid - a)
    ax2.plot(o2primgrid, 2 * o2primgrid + a)
    ax2.plot(o2primgrid, -2 * o2primgrid + a)
    ax2.plot(o2primgrid, -2 * o2primgrid - a)

    ax1.set_ylabel(r"$\Delta_{13}$")
    ax1.set_xlabel(r"$\omega_2'$")
    ax2.set_xlabel(r"$\omega_2'$")
    fig.suptitle("Regions for linear regression Eint12=Eint23=0.04 Eint13=0.0013")
    plt.show()


if __name__ == "__main__":
    # region()
    A = np.array([6.837, 6.589, 6.569, 6.200, 6.107, 6.067, 5.608, 5.588, 5.383, 5.325])
    A = A - 5.325
    print(A * 3.5)
    predict_fig()
    # linear_func(zz12_flat, zz23_flat, zz13_flat, zzz_flat)
    # linear(zz12_flat, zz23_flat, zz13_flat, zzz_flat)
