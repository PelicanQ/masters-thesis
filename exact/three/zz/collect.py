from exact.three.zz.zz import single_zz
import numpy as np
from jobmanager.Handler import Handler3T, Handler3TEnergy
from matplotlib import pyplot as plt, colors
import asyncio
from jobmanager.util import collect_jobs
from store.stores3T import Store_zz3T
from typing import Iterable


def local_collect():
    Ej1s = np.arange(30, 100, 1).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(
        Ec2=1,
        Ec3=1,
        Ej1=Ej1s,
        Ej2=np.arange(30, 100, 1),
        Ej3=50,
        Eint12=0.1,
        Eint23=0.05,
        Eint13=0,
    )
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        if Store_zz3T.check_exists(**job):
            print("exists", job)
            continue
        zz12, zz23, zz13, zzz = single_zz(**job)
        Store_zz3T.insert(**job, zzGS12=zz12, zzGS23=zz23, zzGS13=zz13, zzzGS=zzz)


# using numba enhances gale shapely
# Laptop: Total 15.8. Eig 14.7 Gale 0.7
# runpod  SXM: Total 1.7. Eig 1.1 Gale 0.49


def collect_levels():
    Ejs = np.arange(30, 100, 1).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=Ejs, Ej3=50, Eint12=0.105, Eint23=0.105, Eint13=0.002, k=7)
    H = Handler3TEnergy("http://25.9.103.201:81/3T/energy", [0, 1, 2, 3, 4])
    # test = asyncio.run(H.test_remote())
    # print(test)
    r = asyncio.run(H.submit(jobs, batch_size=2))
    print(r)
    # Store_zz3t.insert_many(r)
    print("Done inserting")


def collect():
    Eints = np.arange(-0.2, 0.2, 0.005).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=89, Ej2=57, Ej3=40, Eint12=Eints, Eint23=Eints, Eint13=0, k=7)
    print("collected", len(jobs))
    filtered = []
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        # if not Store_zz3T.check_exists(**job):
        filtered.append(job)
    print("filtered", len(filtered))
    H = Handler3T("http://25.9.103.201:81/3T")
    # test = asyncio.run(H.test_remote())
    # print(test)
    r = asyncio.run(H.submit(filtered, batch_size=100))
    Store_zz3T.insert_many(r)
    print("Done inserting")


def plot_allzz(var1: Iterable, var2: Iterable, *args):
    # assume the normal order
    varnames = ["zz12", "zz23", "zz13", "zzz"]
    for i in range(len(args)):
        plt.figure()
        plt.pcolor(var1, var2, args[i])
        plt.xlabel("Ej1")
        plt.title(f"{varnames[i]} [Ec1]")
        plt.ylabel("Ej3")
        plt.colorbar()
    # rel = args[-1] - args[0] - args[1] - args[2]
    plt.figure()
    plt.pcolor(var1, var2, rel)
    plt.xlabel("Ej1")
    plt.title(f"rel [Ec1]")
    plt.ylabel("Ej3")
    plt.colorbar()
    plt.show()


def plot_plane():
    Eints = np.arange(-0.2, 0.2, 0.005).tolist()  # numpy types cannot be json serialized
    zz12, zz23, zz13, zzz = Store_zz3T.plane(
        "Eint12", Eints, 3, "Eint23", Eints, 3, Ec2=1, Ec3=1, Ej1=89, Ej2=57, Ej3=40, Eint13=0
    )
    Z = zzz - (zz12 + zz23 + zz13)
    Z = np.abs(Z)
    X, Y = np.meshgrid(Eints, Eints)
    plt.pcolormesh(X, Y, Z, norm=colors.LogNorm(1e-6, 1))
    # plt.pcolor(Ej1s, Ej3s, np.abs(zzz) < 0.01)
    plt.xlabel("Eint12")
    plt.ylabel("Eint23")
    plt.title(f"|ZZZ - all ZZ| [Ec], Ej1=89 Ej2=57 Ej3=40 Eint13=0")
    plt.colorbar()
    plt.show()
    # plot_allzz(Ej1s, Ej3s, zz1, zz2, zz3, zzz)


if __name__ == "__main__":
    plot_plane()
    # collect()
    # plot_plane()
    # collect_levels(
    # vars, zz1, zz2, zz3, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Ej3=2, Eint12=0.1, Eint23=0.1, Eint13=0.1)
    # plt.rc("lines", marker=".", lw=0)
    # plt.plot(vars, zz1, label="zz1", lw=0, marker=".")
    # plt.plot(vars, zz2, label="zz2", lw=0, marker=".")
    # plt.plot(vars, zz3, label="zz3", lw=0, marker=".")
    # plt.plot(vars, zzz, label="zzz", marker=".", lw=0)
    # plt.title("units Ec Ej1=50 Ej3=55, Line layout, Eints=0.2")
    # # plt.title("units Ec, triangle layout, Ej2=50 Ej3=62 Eints=0.1")
    # plt.legend()
    # plt.xlabel("Ej2")
    # plt.show()

# def plane():
#     res = Store_zz3t.plane("Ec2", Ecs, "Ej2", Ejs, Ej1=50, Eint=0.2)
