from exact.threetransmon.zz.zz import single_zz
import numpy as np
from jobmanager.Handler import Handler3T
from matplotlib import pyplot as plt
import asyncio
from jobmanager.util import collect_jobs
from store.store import Store_zz3t


def local_collect():
    Ejs = np.arange(30, 90, 0.5).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=55, Ej3=60, Eint12=0.1, Eint23=0.15, Eint13=0.2)
    for job in jobs:
        zz12, zz23, zz13, zzz = single_zz(**job, k=10)
        # For 3T I only do GS so it's implicit
        Store_zz3t.insert(**job, zzGS12=zz12, zzGS23=zz23, zzGS13=zz13, zzzGS=zzz)


def collect():
    Ejs = np.arange(30, 90, 0.5).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=55, Ej3=60, Eint12=0.1, Eint23=0.15, Eint13=0.2)
    H = Handler3T("http://25.9.103.201:81/3T", k=10)
    r = asyncio.run(H.submit(jobs, batch_size=5))
    Store_zz3t.insert_many(r)
    print("Done inserting")


if __name__ == "__main__":
    local_collect()
    # vars, zz1, zz2, zz3, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=55, Ej3=60, Eint12=0.1, Eint23=0.15, Eint13=0.2)
    # plt.rc("lines", marker=".", lw=0)
    # plt.plot(vars, zz1, label="zz1")
    # plt.plot(vars, zz2, label="zz2")
    # plt.plot(vars, zz3, label="zz3")
    # plt.plot(vars, zzz, label="zzz")
    # plt.legend()
    # plt.title("zz and zzz vs Ej1, other Ej=50, Eint=0.1, Ec=1")
    # plt.xlabel("Ej1")
    # plt.show()

# def plane():
#     res = Store_zz3t.plane("Ec2", Ecs, "Ej2", Ejs, Ej1=50, Eint=0.2)


def line():
    vars, res = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Eint12=0.1, Eint23=0.1, Eint13=0.1)
    print(vars, res)
