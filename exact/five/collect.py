import numpy as np
from jobmanager.util import collect_jobs
from store.stores5T import Store_zz5T_triang
from exact.five.zz import single_zz


def local_collect():
    Ej1 = np.arange(30, 100, 1).tolist()
    Ej2 = np.arange(30, 100, 1).tolist()

    jobs = collect_jobs(
        Ej1=Ej1,
        Ej2=Ej2,
        Ej3=50,
        Ej4=38,
        Ej5=42,
        Eint12=0.1,
        Eint23=0.1,
        Eint13=0.01,
        Eint34=0.1,
        Eint45=0.1,
        Eint35=0.01,
    )
    for i, job in enumerate(jobs):
        print(i, len(jobs))
        if Store_zz5T_triang.check_exists(**job):
            print("exists", job)
            continue
        zz13, zz35, zz15, zzz135 = single_zz(**job)
        Store_zz5T_triang.insert(**job, zz13=zz13, zz35=zz35, zz15=zz15, zzz135=zzz135)


if __name__ == "__main__":
    local_collect()
