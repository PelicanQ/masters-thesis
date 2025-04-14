from exact.threetransmon.zz.zz import single_zz
import numpy as np
from jobmanager.Handler import Handler3T, Handler3TEnergy
from matplotlib import pyplot as plt
import asyncio
from jobmanager.util import collect_jobs
from store.stores import Store_zz3T
from typing import Iterable


def local_collect():
    Ejs = np.arange(30, 80, 0.5).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(
        Ec2=1,
        Ec3=1,
        Ej1=Ejs,
        Ej2=50,
        Ej3=50,
        Eint12=0.1,
        Eint23=0.1,
        Eint13=0.1,
        k=8,
    )
    for i, job in enumerate(jobs):
        print(job)
        print(i, len(jobs))
        # t = time.perf_counter()
        zz12, zz23, zz13, zzz = single_zz(**job)
        # print("total", time.perf_counter() - t)
        # For 3T I only do GS so it's implicit
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
    Ejs = np.arange(30, 90, 0.5).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(
        Ec2=1, Ec3=1, Ej1=Ejs, Ej2=50, Ej3=np.arange(60, 70, 0.5), Eint12=0.1, Eint23=0.1, Eint13=0.1, k=8
    )
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
    Ej1s = np.arange(30, 90, 0.5)
    Ej3s = np.arange(30, 70, 0.5)

    zz1, zz2, zz3, zzz = Store_zz3T.plane(
        "Ej1", Ej1s, "Ej3", Ej3s, Ec2=1, Ec3=1, Ej2=50, Eint12=0.1, Eint23=0.1, Eint13=0.1
    )
    plt.pcolor(Ej1s, Ej3s, np.abs(zzz - (zz1 + zz2 + zz3)) < 0.01)
    # plt.pcolor(Ej1s, Ej3s, np.abs(zzz) < 0.01)
    plt.xlabel("Ej1")
    plt.title(f"rel [Ec1]")
    plt.ylabel("Ej3")
    plt.colorbar()
    plt.show()
    # plot_allzz(Ej1s, Ej3s, zz1, zz2, zz3, zzz)


if __name__ == "__main__":
    # local_collect()
    plot_plane()
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
