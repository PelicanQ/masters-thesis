from exact.threetransmon.zz.zz import single_zz
import numpy as np
from jobmanager.Handler import Handler3T
from matplotlib import pyplot as plt
import asyncio
from jobmanager.util import collect_jobs
from store.store import Store_zz3t

def local_collect():
    Ejs = np.arange(30, 90, 10)
    jobs = collect_jobs(Ec2=1,Ec3=1, Ej1=Ejs, Ej2=50, Ej3=50, Eint12=0.1,Eint23=0.1,Eint13=0.1)
    for job in jobs:
        zz12, zz23, zz13, zzz = single_zz(**job, k=10)
        # For 3T I only do GS so it's implicit
        Store_zz3t.insert(**job, zzGS12=zz12, zzGS23=zz23, zzGS13=zz13, zzzGS=zzz)

def collect():
    Ejs = np.arange(30, 90, 1).tolist()  # numpy types cannot be json serialized
    Ecs = np.arange(0.4, 1.4, 0.2).tolist()
    Eints = np.arange(0.05, 0.8, 0.1).tolist()
    jobs = collect_jobs(Ej1=50, Ej2=Ejs, Eint=Eints, Ec2=Ecs)
    
    H = Handler3T("http://25.9.103.201:82/2T", k=12)
    r = asyncio.run(H.submit(jobs, batch_size=50))
    Store_zz3t.insert_many(r)
    
    print("Done inserting")

if __name__ == "__main__":
    local_collect()


# def plane():
#     res = Store_zz3t.plane("Ec2", Ecs, "Ej2", Ejs, Ej1=50, Eint=0.2)


def line():
    vars, res = Store_zz3t.line(Ec2=1,Ec3=1,Ej2=50, Eint12=0.1,Eint23=0.1,Eint13=0.1)
    print(vars, res)


