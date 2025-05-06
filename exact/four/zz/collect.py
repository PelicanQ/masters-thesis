from exact.four.zz.zz import single_zz
import numpy as np

# from jobmanager.Handler import Handler4T
from matplotlib import pyplot as plt
import asyncio
from jobmanager.util import collect_jobs
from store.stores4T import Store_zz4T
from typing import Iterable
from other.colormap import Norm, OrBu_colormap


def local_collect():
    Ej1s = np.arange(30, 100, 4).tolist()  # numpy types cannot be json serialized
    jobs = collect_jobs(
        Ej1=Ej1s,
        Ej2=Ej1s,
        Ej3=50,
        Ej4=56.5,
        Eint12=0.085,
        Eint23=0.085,
        Eint13=0.0046,
        Eint34=0.085,
    )
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        if Store_zz4T.check_exists(**job):
            print("exists")
            continue
        result = single_zz(**job)
        Store_zz4T.insert(**job, **result)


# def collect():
#     Ejs = np.arange(30, 100, 0.5).tolist()  # numpy types cannot be json serialized
#     jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=Ejs, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.01, k=7)
#     print("collected", len(jobs))
#     filtered = []
#     for i, job in enumerate(jobs):
#         print(i, len(jobs))
#         if not Store_zz4T.check_exists(**job):
#             filtered.append(job)
#     print("filtered", len(filtered))
#     H = Handler4T("http://25.9.103.201:81/3T")
#     # test = asyncio.run(H.test_remote())
#     # print(test)
#     r = asyncio.run(H.submit(filtered, batch_size=100))
#     Store_zz4T.insert_many(r)
#     print("Done inserting")


def plot_plane():
    Ejs = np.arange(30, 100, 4).tolist()  # numpy types cannot be json serialized
    results = Store_zz4T.plane(
        "Ej2", Ejs, 1, "Ej1", Ejs, 1, Ej3=50, Ej4=50, Eint12=0.1, Eint23=0.1, Eint13=0.002, Eint34=0.1
    )
    plt.pcolor(Ejs, Ejs, results["zz13"], norm=Norm(1e-1), cmap=OrBu_colormap())
    # plt.pcolor(Ej1s, Ej3s, np.abs(zzz) < 0.01)
    plt.title(f"asdfasdfads")
    plt.xlabel("Ej2")
    plt.ylabel("Ej1")
    plt.colorbar()
    plt.show()
    # plot_allzz(Ej1s, Ej3s, zz1, zz2, zz3, zzz)


if __name__ == "__main__":
    # local_collect()
    plot_plane()
