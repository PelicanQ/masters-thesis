# let's see when the ground level stablizes with k. I wanna keep k low due to slow numerics
import numpy as np
from exact.threetransmon.zz.zz import single_zz_energy
from matplotlib import pyplot as plt
from jobmanager.Handler import Handler3TEnergy
import asyncio
import time

level_select = [0, 1, 2, 3, 4, 10, 20, 30, 40, 50]
kk = np.arange(5, 10, 1)
Ej1 = 50
Ej2 = 60
Ej3 = 45
Eint12 = 0.2
Eint23 = 0.3
Eint13 = 0.3


def save(results):
    ks = np.zeros_like(kk)
    Es = []
    for i, res in enumerate(results):
        ks[i] = res["k"]
        Es.append(res["levels"])
    inds = np.argsort(ks)
    ks = ks[inds]
    sortE = [Es[i] for i in inds]
    np.save("3Tkconv_kk2", ks)
    np.save("3Tkconv_Es2", np.array(sortE).T)


def local_collect():
    ks = np.zeros_like(kk)
    Es = np.zeros((len(level_select), len(ks)))
    for i, k in enumerate(kk):
        ks[i] = k
        t = time.perf_counter()
        levels = single_zz_energy(1, 1, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=k)
        print(f"Time: ", time.perf_counter() - t)
        Es[:, i] = levels[level_select]
    np.save("3Tkconv_kk2", ks)
    np.save("3Tkconv_Es2", Es)


# 3T energy time: (k, laptop time): (8,2) (9,3) (10, 8) (11, 26) (12, 317)
# There must be some memory cieling we hit. k=12 means 15625 x 15625 total Hamil
def collect_kk():
    H = Handler3TEnergy("http://25.9.103.201:81/3T/energy", level_select)
    jobs = [
        {
            "k": k,
            "Ec2": 1,
            "Ec3": 1,
            "Ej1": 50,
            "Ej2": 60,
            "Ej3": 45,
            "Eint12": 0.2,
            "Eint23": 0.3,
            "Eint13": 0.3,
        }
        for k in kk.tolist()
    ]
    results = asyncio.run(H.submit(jobs, 3))
    save(results)


if __name__ == "__main__":
    local_collect()
    # kk = np.load("3Tkconv_kk2.npy")
    # Es = np.load("3Tkconv_Es2.npy")
    # for i in range(len(Es)):
    #     plt.figure()
    #     plt.plot(kk, Es[i, :])
    #     plt.title(f"Level {level_select[i]} [Ec1]")
    #     plt.xlabel("k")
    # plt.show()
