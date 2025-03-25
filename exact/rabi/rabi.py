import matplotlib.pyplot as plt
import numpy as np
from qutip import *

omega0 = 1
omega1 = 0.5
omega = 1
Hgen = lambda t, args: 0.5 * Qobj(
    [
        [omega0, omega1 * np.exp(-1j * omega * t)],
        [omega1 * np.exp(1j * omega * t), -omega0],
    ]
)
H = QobjEvo(Hgen)

init = basis(2, 0)
T = 300
tt = np.linspace(0, 50, T)
r = sesolve(H, init, tt)
# r = sesolve(H, init, tt, e_ops=sigmaz())

a = [abs(state.overlap(basis(2, 0))) ** 2 for state in r.states]
prob = [abs(state.overlap(basis(2, 1))) ** 2 for state in r.states]

# print(r.states)
# plt.plot(r.expect[0])
# plt.plot(a)
plt.plot(prob)


#
#
# now lets plot probability up/down over time for different omega

M = 70
c = np.zeros(shape=(T, M))
for idx, omega in enumerate(np.linspace(-0.5, 3, M)):
    Hgen = lambda t: 0.5 * Qobj(
        [
            [omega0, omega1 * np.exp(-1j * omega * t)],
            [omega1 * np.exp(1j * omega * t), -omega0],
        ]
    )
    H = QobjEvo(Hgen)
    r = sesolve(H, init, tt)
    prob = [abs(state.overlap(basis(2, 1))) ** 2 for state in r.states]
    c[:, idx] = prob

plt.figure()
plt.imshow(c, aspect=0.15, origin="lower")
plt.title("Probability of state 1")
plt.xlabel("Omega")
plt.ylabel("Time")
plt.colorbar()
plt.show()
