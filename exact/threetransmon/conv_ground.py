# let's see when the ground level stablizes with k. I wanna keep k low due to slow numerics
import numpy as np
from exact.threetransmon.hamil import eig_clever
from matplotlib import pyplot as plt
from jobmanager.Handler import Handler3TEnergy
import asyncio

level_select = [0, 1, 2, 3, 4, 10, 20, 30, 40, 50]


def collect_kk():
    kk = np.arange(5, 12, 1)
    ks = np.zeros_like(kk)
    Es = []

    H = Handler3TEnergy("http://25.9.103.201:81/3T/energy", level_select)
    results = asyncio.run(
        H.submit(
            [
                {
                    "k": k,
                    "Ec2": 1,
                    "Ec3": 1,
                    "Ej1": 50,
                    "Ej2": 50,
                    "Ej3": 50,
                    "Eint12": 0.1,
                    "Eint23": 0.1,
                    "Eint13": 0.1,
                }
                for k in kk.tolist()
            ],
            3,
        )
    )

    print("the res")
    for i, res in enumerate(results):
        print(ks[i])
        ks[i] = res["k"]
        Es.append(res["levels"])
        print(res)
    inds = np.argsort(ks)
    ks = ks[inds]
    sortE = [Es[i] for i in inds]
    np.save("3Tkconv_kk", ks)
    np.save("3Tkconv_Es", np.array(sortE).T)


if __name__ == "__main__":
    # collect_kk()
    kk = np.load("3Tkconv_kk.npy")
    Es = np.load("3Tkconv_Es.npy")
    for i in range(len(Es)):
        plt.figure()
        plt.plot(kk, Es[i, :])
        plt.title(f"Level {level_select[i]} [Ec1]")
        plt.xlabel("k")
    plt.show()
