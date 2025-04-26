from onetransmon.hamil import ng_sweep, ngs
from matplotlib.axes import Axes
from matplotlib import pyplot as plt

fig, axes = plt.subplots(2, 2)
ax1: Axes = axes[0][0]
ax2: Axes = axes[0][1]
ax3: Axes = axes[1][0]
ax4: Axes = axes[1][1]

evals = ng_sweep(1)
ax1.plot(ngs, evals[0, :])
ax1.plot(ngs, evals[1, :])
ax1.plot(ngs, evals[2, :])
ax1.set_title("1")

evals = ng_sweep(5)
ax2.plot(ngs, evals[0, :])
ax2.plot(ngs, evals[1, :])
ax2.plot(ngs, evals[2, :])
ax2.set_title("5")

evals = ng_sweep(10)
ax3.plot(ngs, evals[0, :])
ax3.plot(ngs, evals[1, :])
ax3.plot(ngs, evals[2, :])
ax3.set_title("10")

evals = ng_sweep(50)
ax4.plot(ngs, evals[0, :])
ax4.plot(ngs, evals[1, :])
ax4.plot(ngs, evals[2, :])
ax4.set_title("50")

fig.suptitle("Eigenenergies of DC-SQUID at different $E_J/E_C$")
ax3.set_xlabel("$n_g$")
ax3.set_ylabel("Eigenvalue")
plt.show()
