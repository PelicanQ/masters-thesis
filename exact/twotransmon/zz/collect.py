import numpy as np
from jobmanager.Handler import Handler2T, Handler2TEnergy
from jobmanager.util import collect_jobs
from store.stores import Store_zz2t
from exact.twotransmon.zz.zz import single_zz
from matplotlib import pyplot as plt
import asyncio


def local_collect():
    Ejs = np.arange(30, 90, 0.2)
    Eints = np.arange(0, 0.8, 0.02)
    jobs = collect_jobs(Ej1=Ejs, Ej2=50, Eint=Eints, Ec2=1)
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        zz, zzGS = single_zz(**job, k=8)
        Store_zz2t.insert(**job, zz=zz, zzGS=zzGS)


if __name__ == "__main__":
    Ec = np.arange(0.1, 2, 0.01)
    Ej = np.arange(0, 80, 0.1)
    jobs = collect_jobs(Ej1=50, Ej2=Ec, Eint=3, Ec2=Ec, k=8)
    print(len(jobs))
    # local_collect()

    H = Handler2TEnergy("http://25.9.103.201:81/2T")
    # H = Handler2T("http://25.9.103.201:81/2T")
    r = asyncio.run(H.submit(jobs, batch_size=400))
    Store_zz2t.insert_many(r)
    print("Done inserting")


def plane():
    zz, zzGS = Store_zz2t.plane("Ec2", Ecs, "Ej2", Ejs, Ej1=50, Eint=0.2)
    plt.pcolor(Ecs, Ejs, zzGS)
    plt.xlabel("Ec2")
    plt.ylabel("Ej2")
    plt.colorbar()
    plt.title("Numeric zz unit Ec1, Ej1=50, Eint=0.2")
    plt.show()


def line():
    vars, zz, zzGS = Store_zz2t.line(Ej1=60, Ej2=50, Eint=0.2)
    plt.plot(vars, zzGS, lw=0, marker=".")
    plt.xlabel("Ec")
    plt.ylabel("Ec")
    plt.show()


# plane()
