# let's see when the ground level stablizes with k. I wanna keep k low due to slow numerics
import numpy as np
from exact.threetransmon.hamil import eig_clever
from matplotlib import pyplot as plt
from jobmanager.Handler import Handler3TEnergy
import asyncio

E = []
H = Handler3TEnergy("http://25.9.103.201:81/3T/energy", [0, 1, 2, 3, 4])
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
            for k in np.arange(5, 10, 1).tolist()
        ],
        3,
    )
)
for r in results:
    print(r)

# plt.plot(kk, vals)
# plt.show()
