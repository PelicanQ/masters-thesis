from exact.three.zz.zz import single_zz
import numpy as np
from jobmanager.Handler import Handler3T, Handler3TEnergy
from matplotlib import pyplot as plt, colors
import asyncio
from jobmanager.util import collect_jobs
from store.stores3T import Store_zz3T
from typing import Iterable
from other.colormap import Norm, OrBu_colormap


def local_collect():
    Ejs = np.arange(56, 62, 0.1).tolist()  # numpy types cannot be json serialized
    # Eints = np.arange(0.02, 0.06, 0.01).tolist()
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=50, Ej2=Ejs, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.035)
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        if Store_zz3T.check_exists(**job):
            print("exists", job)
            continue
        zz12, zz23, zz13, zzz = single_zz(**job)
        Store_zz3T.insert(**job, zzGS12=zz12, zzGS23=zz23, zzGS13=zz13, zzzGS=zzz)


def collect_levels():
    Ejs = np.arange(56, 62, 0.1).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=50, Ej2=Ejs, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.035)
    H = Handler3TEnergy("http://25.9.103.201:81/3T/energy", [0, 1, 2, 3, 4])
    # test = asyncio.run(H.test_remote())
    # print(test)
    r = asyncio.run(H.submit(jobs, batch_size=2))
    print(r)
    # Store_zz3t.insert_many(r)
    print("Done inserting")


E = 0.04
E13 = 0.0013


def collect():
    Ejs = np.arange(30, 100, 1).tolist()
    Ejs2 = np.arange(30, 140, 0.1).tolist()
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=50, Ej2=Ejs2, Ej3=50, Eint12=E, Eint23=E, Eint13=E13, k=7)
    print("collected", len(jobs))
    filtered = Store_zz3T.filter_existing(jobs)
    print("Before", len(jobs))
    print("After filter", len(filtered))
    H = Handler3T("http://25.9.103.201:81/3T")
    # test = asyncio.run(H.test_remote())
    # print(test)
    r = asyncio.run(H.submit(filtered, batch_size=100))
    Store_zz3T.insert_many(r)
    print("Done inserting. ", len(r))


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
    Ejs = np.arange(45, 60, 1)
    Ejs2 = np.arange(60, 100, 1)
    zz12, zz23, zz13, zzz = Store_zz3T.plane(
        "Ej2", Ejs2, 1, "Ej1", Ejs, 1, Ec2=1, Ec3=1, Ej3=50, Eint12=E, Eint23=E, Eint13=E13
    )
    plt.pcolor(Ejs2, Ejs, zz13, cmap=OrBu_colormap(), norm=Norm(1e-1))
    plt.title(f"ZZ13 [Ec]")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    # local_collect()
    # plot_line()
    collect()
    # plot_plane()


def plot_line():
    vars, zz12, zz23, zz13, zzz = Store_zz3T.line(Ec2=1, Ec3=1, Ej1=50, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.035)
    # plt.rc("lines", marker=".", lw=0, markersize=5)
    plt.rc("lines", markersize=5)
    plt.semilogy(vars, np.abs(zz13), label="zz13")
    plt.semilogy(vars, np.abs(zzz), label="zzz")
    # plt.yscale("symlog", linthresh=1e-5)
    plt.title("Magnitude of ZZZ and ZZ13 Ej1=Ej3=50 E12=E23=0.1 E13=0.035. Units Ec")
    # plt.title("units Ec, triangle layout, Ej2=50 Ej3=62 Eints=0.1")
    plt.legend()
    plt.xlabel("Ej2")
    plt.ylabel("Magnitude [Ec]")
    plt.show()
