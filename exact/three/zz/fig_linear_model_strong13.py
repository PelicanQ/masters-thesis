from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from store.stores3T import Store_zz3T
from exact.util import omega_alphas
from matplotlib import pyplot as plt, colors
import scienceplots

plt.style.use(["science", "nature"])
Ej3 = 50
Ej1s = np.arange(30, 100, 0.2)
Ej2s = np.arange(30, 140, 0.2)

E = 0.04
Eint13 = 0.008
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=E, Eint23=E, Eint13=Eint13, Ec2=1, Ec3=1
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


def predict_fig():

    a12 = 1.00314978  # 0.99501465
    a23 = 1.06638546
    a13 = 4.09027235

    pred111 = zz12 + zz23 + zz13
    preda = a12 * zz12 + a23 * zz23 + a13 * zz13
    rel111 = np.abs(zzz - pred111) / np.abs(zzz)
    rela = np.abs(zzz - preda) / np.abs(zzz)

    fig, ax1 = plt.subplots(1, 1, sharex=True, sharey=True, constrained_layout=True, figsize=(5.9, 5.9 * 3 / 4))

    colorss = plt.cm.Oranges(np.linspace(0, 0.8, 20))

    cmap = colors.LinearSegmentedColormap.from_list("my_colormap", colorss)
    for x in np.arange(-20, 20, 1):
        ax1.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)
        # ax2.axline(xy1=(x, 0), color="lightgray", linestyle="-", linewidth=0.8, zorder=0, slope=-2)
    # ax2.axline(x=xg, color="gray", linestyle="-", linewidth=0.5, zorder=0)

    c = ax1.pcolormesh(o2primgrid, detunegrid, rel111, vmin=0.01, vmax=0.1, cmap=cmap, zorder=1)
    # ax2.pcolormesh(o2primgrid, detunegrid, rela, vmin=0.01, vmax=0.1, cmap=cmap)

    fig.suptitle(f"Relative ZZZ prediciton error for $E_{{J3}}={Ej3}$  $E_{{12}}=E_{{23}}={E}$ $E_{{13}}={Eint13}$ ")
    ax1.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
    ax1.set_xlabel(r"$\omega_2'$ [$E_C$]")
    ax1.set_ylim([-4, 8])
    ax1.set_xlim([-6, 14])
    # ax2.set_ylabel(r"$\Delta_{13}$ [$E_C$]")
    fig.colorbar(c, ax=[ax1])
    fig.savefig("figs/linear-model-error-strong13.png", dpi=300, bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    predict_fig()
    # 111 57.03
    # 201 56.47
    # 210 56.27
    # 102 56.06
    # 120 55.67
    # 012 55.47
    # 021 55.27
    # 300 54.45
    # 003 53.24
    # 030 52.63
    # A = np.array([57.03, 56.47, 56.27, 56.06, 55.67, 55.47, 55.27, 54.45, 53.24, 52.63])
    # A = A - 52.63
    # A = A / np.max(A) * 5.292
    # print(A)
