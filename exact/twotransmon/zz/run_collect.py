from exact.twotransmon.collect import collect_sweep, collect_jobs, Store_zz2t
import numpy as np
from jobmanager.Handler import Handler
from matplotlib import pyplot as plt
import asyncio

Ejs = np.arange(30, 100, 2)
Ecs = np.arange(0.2, 10, 0.1)
if __name__ == "__main__":
    jobs = collect_jobs(Ej1=50, Ej2=[40, 50], Eint=0.2, Ec2=[1, 2])
    print("all jobs", jobs)
    H = Handler("http://25.9.103.201:82/2T", k=40)
    r = asyncio.run(H.submit(jobs, batch_size=2))
    print("DONE", r)
    # Store_zz2t.insert_many(r)

    # collect_sweep(13, Ej1=50, Ej2=Ejs, Eint=0.2, Ec2=Ecs)


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
