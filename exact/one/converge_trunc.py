from exact.one.hamil import calc_eigs, plt
import numpy as np
import cupy as cp

# How do the energy levels change with different truncation
# We try different Ej
kk = np.concatenate([np.arange(start=6, stop=20, step=1), np.arange(start=22, stop=50, step=4)])


def run(Ej):
    E = np.zeros(shape=(13, len(kk)))
    # 13 = 2*6+1
    for i, k in enumerate(kk):
        vals = calc_eigs(Ej, ng=0, k=k)
        E[:, i] = vals[:13] - vals[0]

    low_cut = 15  # lower cut for std

    plt.figure(figsize=(12, 6))

    # now make a subplot for each energy level relative to lowest
    diffs = [1, 2, 3, 6, 11, 12]
    stds = []
    for i, d in enumerate(diffs):
        energy = E[d, :]
        std = np.std(energy[low_cut:])
        stds.append(std)

        plt.subplot(2, 3, i + 1)
        plt.plot(kk, energy, marker=".", label=f"E{d}")
        plt.axvline(x=kk[low_cut], color="r", linestyle="--", label="low_cut")
        plt.title(f"std=10^{np.log10(std):.0f}", fontsize=7)
        plt.xlabel("k")
        plt.ylabel(f"E{d}(k)-E0(k)")
        plt.tight_layout(pad=0.7)  # Adjust the padding between plots

    plt.subplots_adjust(top=0.85)  # Adjust the top to make space for suptitle
    plt.suptitle(f"Convergence of energy levels, Ej={Ej}, dashed line is low_cut={kk[low_cut]}")


run(200)

plt.show()
