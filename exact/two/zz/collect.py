import numpy as np
from jobmanager.Handler import Handler2T, Handler2TEnergy
from jobmanager.util import collect_jobs
from store.stores import Store_zz2T, StoreLevels2T
from exact.twotransmon.zz.zz import single_zz
from matplotlib import pyplot as plt
import asyncio


def local_collect():
    Ejs = np.arange(30, 90, 1)
    Ec = np.arange(0, 2, 0.1)
    jobs = collect_jobs(Ej1=50, Ej2=Ejs, Eint=0.3, Ec2=Ec)
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        zz, zzGS = single_zz(**job, k=8)
        Store_zz2T.insert(**job, zz=zz, zzGS=zzGS)


def plane():
    Ec = np.arange(0.1, 2, 0.02)
    Ej = np.arange(30, 140, 0.5)
    zz, zzGS = Store_zz2T.plane("Ec2", Ec, "Ej2", Ej, Ej1=50, Eint=0.3)
    plt.pcolor(Ec, Ej, zzGS)
    plt.xlabel("Ec2")
    plt.ylabel("Ej2")
    plt.colorbar()
    plt.title("Numeric zz [Ec1], Ej1=50, Eint=0.3")
    plt.show()


def line():
    vars, zz, zzGS = Store_zz2T.line(Ej1=60, Ej2=50, Eint=0.2)
    plt.plot(vars, zzGS, lw=0, marker=".")
    plt.xlabel("Ec")
    plt.ylabel("Ec")
    plt.show()


if __name__ == "__main__":
    plane()
    exit()
    Ec = np.arange(0.1, 2, 0.02).tolist()
    Ej = np.arange(30, 140, 0.5).tolist()
    jobs = collect_jobs(Ej1=50, Ej2=Ej, Eint=0.3, Ec2=Ec, k=8)
    print(len(jobs))
    # local_collect()

    # H = Handler2TEnergy("http://25.9.103.201:81/2T/energy", list(range(8)))
    # StoreLevels2T.insert_many(r)
    H = Handler2T("http://25.9.103.201:81/2T")
    r = asyncio.run(H.submit(jobs, batch_size=400))
    Store_zz2T.insert_many(r)
    print("Done inserting")
