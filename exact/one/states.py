from onetransmon.hamil import Hgen, plt, Axes, nstates, np

# What are the eigenstates like? Check their coordinates
ng = 0.5
ratio = 20
eig = np.linalg.eig(Hgen(ng, ratio))
idx = np.argsort(eig.eigenvalues)
vecs = eig.eigenvectors[:, idx]
vals = eig.eigenvalues[idx]
# sorted

fig, axes = plt.subplots(2, 1)
ax1: Axes = axes[0]
ax2: Axes = axes[1]

ax1.plot(nstates, vecs[:, 0], marker=".", label="0")
ax1.plot(nstates, vecs[:, 20], marker=".", label="20")
ax1.plot(nstates, vecs[:, 50], marker=".", label="50")
ax1.plot(nstates, vecs[:, 51], marker=".", label="51")
ax1.plot(nstates, vecs[:, 90], marker=".", label="90")
ax1.legend()
ax1.set_title(f"(n-space) Coordinates of some eigenstates v for ratio {ratio}, ng {ng}")
ax1.set_ylabel("v[i]")
ax1.set_xlabel("i")


# now lets fourier to get the wavefunction in position (phi) space
def coeff2val(x, coeff: np.ndarray):
    # coeff should have odd number entries (one 0 frequency)
    num = coeff.size // 2
    n = np.arange(-num, num + 1, step=1)

    return np.sum(np.multiply(np.exp(1j * n * x), coeff)) / (2 * np.pi)


res = 120  # resolution
y0 = np.empty(res)
y1 = np.empty(res)
y2 = np.empty(res)
xx = np.linspace(-np.pi, np.pi, res)

for i, x in enumerate(xx):
    y1[i] = 80 * np.abs(coeff2val(x, vecs[:, 1])) ** 2 + vals[1] - vals[0]
    y0[i] = 80 * np.abs(coeff2val(x, vecs[:, 0])) ** 2
    y2[i] = 80 * np.abs(coeff2val(x, vecs[:, 2])) ** 2 + vals[2] - vals[0]

ax2.plot(xx, y0)
ax2.plot(xx, y1)
ax2.plot(xx, y2)
ax2.plot(xx, -20 * np.cos(xx) + 20)
ax2.set_xlabel("phi")
ax2.set_ylabel("probability density")

plt.show()
