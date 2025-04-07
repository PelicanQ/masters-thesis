from pathlib import Path
from exact.twotransmon.zz.sweep import single_zz
from exact.twotransmon.hamil import eig_clever
import numpy as np
from store.store import Store_zz2t
from matplotlib import pyplot as plt
from analysis.plot import plot, grid3d
import itertools
from jobmanager.Handler import Handler


def get_iterable_keys(kwargs):
    # intended for when one key is iterable
    iterable_names = []
    for key, val in kwargs.items():
        try:
            iter(val)
            iterable_names.append(key)
        except:
            pass
    if len(iterable_names) == 0:
        raise Exception("You need some iterable")
    return iterable_names


def collect_jobs(**kwargs):
    # find iterables among given kwargs, loop over them and run zz
    iterables = get_iterable_keys(kwargs)
    arguments = kwargs.copy()
    jobs: list[dict] = []
    for tup in itertools.product(*[kwargs[itkey] for itkey in iterables]):
        # tuple now contains one point in the grid
        items = [(iterables[i], tup[i]) for i in range(len(iterables))]  # list of (key, value) pairs
        arguments.update(items)  # update the changing parameters
        jobs.append(arguments.copy())
    return jobs


def collect_sweep(k, **kwargs):
    # find iterables among given kwargs, loop over them and run zz
    iterables = get_iterable_keys(kwargs)
    arguments = kwargs.copy()
    for tup in itertools.product(*[kwargs[itkey] for itkey in iterables]):
        # tuple now contains one point in the grid
        items = [(iterables[i], tup[i]) for i in range(len(iterables))]  # list of (key, value) pairs
        arguments.update(items)  # update the changing parameters
        zz, zzGS = single_zz(**arguments, k=k)

        Store_zz2t.insert(**arguments, zz=zz, zzGS=zzGS)


def collect():
    # Collection of data into SQLite
    k = 13
    Ec2 = 1
    Eints = np.arange(0.1, 1, 1)
    Ej1s = np.arange(30, 90, 1)
    Ej2s = np.arange(50, 51, 10)
    for Eint in Eints:
        for Ej2 in Ej2s:
            for Ej1 in Ej1s:
                zz, zzGS = single_zz(Ej1s=Ej1s, Ej2=Ej2, Eint=Eint, Ec2=Ec2, k=k, ng1=0)
                Store_zz2t.insert(Ec2, Ej1, Ej2, Eint, zz, zzGS)

    # 0.14 seconds per run


if __name__ == "__main__":
    a = np.arange(0.2, 1.5, 0.1)
    b = np.arange(0, 1, 0.05)
    # collect_sweep(13, Ec2=a, Ej1=np.arange(40, 60, 2), Ej2=50, Eint=b)
    eints, zz, zzgs = Store_zz2t.plane("Ec2", a, "Eint", b, Ej1=50, Ej2=50)
    # eints, zz2, zzgs2 = Store_zz2t.line(Ec2=1, Ej1=80, Ej2=50)
    # plt.rc("lines", marker=".")
    # plot(eints, zzgs, "Eint", "ZZ", "ZZ vs Eint")
    # plt.plot(eints, zzgs2)
    # plt.show()
