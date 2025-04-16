from exact.threetransmon.zz.zz import single_zz
import numpy as np
from jobmanager.Handler import Handler3T, Handler3TEnergy
from matplotlib import pyplot as plt
import asyncio
from jobmanager.util import collect_jobs
from store.stores import Store_zz3T
from typing import Iterable


def local_collect():
    Ej1s = np.arange(30, 80, 1).tolist()  # numpy types cannot be json serialized

    Ej2s = np.arange(30, 80, 0.2).tolist()  # numpy types cannot be json serialized
    Ej2s = list(filter(lambda n: abs(n - round(n)) > 1e-4, Ej2s))
    jobs = collect_jobs(
        Ec2=1,
        Ec3=1,
        Ej1=Ej1s,
        Ej2=Ej2s,
        Ej3=50,
        Eint12=0.1,
        Eint23=0.1,
        Eint13=0,
        k=8,
    )
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        zz12, zz23, zz13, zzz = single_zz(**job)
        Store_zz3T.insert(**job, zzGS12=zz12, zzGS23=zz23, zzGS13=zz13, zzzGS=zzz)


# using numba enhances gale shapely
# Laptop: Total 15.8. Eig 14.7 Gale 0.7
# runpod  SXM: Total 1.7. Eig 1.1 Gale 0.49


def collect_levels():
    Ejs = np.arange(30, 90, 10).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=55, Ej3=60, Eint12=0.1, Eint23=0.15, Eint13=0.2, k=3)
    H = Handler3TEnergy("http://25.9.103.201:81/3T/energy", [0, 1, 2, 3, 4])
    # test = asyncio.run(H.test_remote())
    # print(test)
    r = asyncio.run(H.submit(jobs, batch_size=2))
    print(r)
    # Store_zz3t.insert_many(r)
    print("Done inserting")


def collect():
    Ejs = np.arange(30, 80, 0.5).tolist()  # numpy types cannot be json serialized
    Eints = np.arange(0, 0.8, 0.05).tolist()
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=50, Ej3=140, Eint12=Eints, Eint23=0.2, Eint13=0, k=8)
    H = Handler3T("http://25.9.103.201:81/3T")
    # test = asyncio.run(H.test_remote())
    # print(test)
    r = asyncio.run(H.submit(jobs, batch_size=20))
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
    Ejs = np.arange(30, 80, 0.5).tolist()  # numpy types cannot be json serialized
    Eints = np.arange(0, 0.8, 0.05)
    zz12, zz2, zz3, zzz = Store_zz3T.plane(
        "Ej1", Ejs, "Eint12", Eints, Ec2=1, Ec3=1, Ej2=50, Ej3=140, Eint23=0.2, Eint13=0
    )
    plt.pcolor(Ejs, Eints, zz12)
    # plt.pcolor(Ej1s, Ej3s, np.abs(zzz) < 0.01)
    plt.xlabel("Ej1")
    plt.title(f"zz12 [Ec1], Line, Ej3=140 Ej2=50 Eint23=0.2 ")
    plt.ylabel("Eint12")
    plt.colorbar()
    plt.show()
    # plot_allzz(Ej1s, Ej3s, zz1, zz2, zz3, zzz)


if __name__ == "__main__":
    # collect()
    local_collect()
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
