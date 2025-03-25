import matplotlib.pyplot as plt
import numpy as np
from qutip import *

# see guide to sc qubit, equation 107
# two capacitively coupled qubits with same frequency. coupling g

# Now probability grid

T = 400  # time resolution
tt = np.linspace(0, 40, T)

M = 200  # resolution of parameter axis
c = np.zeros(shape=(T, M))  # image
g = 0.5
init = basis(4, 1)
stateobs = 2  # state probability to look at

for idx, delta in enumerate(np.linspace(-4, 4, M)):
    Hgenplus = lambda t: g * Qobj(
        [
            [0, 0, 0, 0],
            [0, 0, np.exp(-1j * delta * t), 0],
            [0, np.exp(1j * delta * t), 0, 0],
            [0, 0, 0, 0],
        ]
    )
    # Hgenminus = lambda t: g * Qobj(
    #     [
    #         [0, 0, 0, 1],
    #         [0, 0, 0, 0],
    #         [0, 0, 0, 0],
    #         [1, 0, 0, 0],
    #     ]
    # )
    H = QobjEvo(Hgenplus)
    r = sesolve(H, init, tt)
    prob = [abs(state.overlap(basis(4, stateobs))) ** 2 for state in r.states]
    c[:, idx] = prob

plt.imshow(c, aspect=1, origin="lower")
plt.title(f"Probability of state {stateobs}")
plt.xlabel("Delta")
plt.ylabel("Time")
plt.colorbar()
plt.show()
