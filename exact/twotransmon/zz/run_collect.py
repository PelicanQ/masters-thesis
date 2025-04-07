from exact.twotransmon.collect import collect_sweep, collect_jobs, Store_zz2t
import numpy as np
from jobmanager.Handler import Handler
from matplotlib import pyplot as plt
import asyncio


if __name__ == "__main__":
    Ejs = np.arange(30, 90, 1).tolist()  # numpy types cannot be json serialized
    Ecs = np.arange(0.4, 1.4, 0.2).tolist()
    Eints = np.arange(0.05, 0.8, 0.1).tolist()
    jobs = collect_jobs(Ej1=50, Ej2=Ejs, Eint=Eints, Ec2=Ecs)
    H = Handler("http://25.9.103.201:82/2T", k=12)
    r = asyncio.run(H.submit(jobs, batch_size=50))
    Store_zz2t.insert_many(r)
    print("Done inserting")

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
