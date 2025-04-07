from matplotlib import pyplot as plt
import numpy as np
from ..store import Store


# Let's see how the lowest energy levels change with different truncation
# Here we have a fixed Ej
def conv(
    store: Store,
    levels: list[int, int, int, int],
    Ej_indices: list[int, int, int, int],
):
    kk = store.kk
    Ejs = store.Ejs

    low_cut = 5  # lower cut for std
    print("Checking levels ", levels, " with Ej ", [Ejs[i] for i in Ej_indices])

    plt.figure(figsize=(12, 6))
    for j, Ej_idx in enumerate(Ej_indices):
        Ej = Ejs[Ej_idx]
        plt.subplot(2, 2, j + 1)
        for level in levels:
            E0 = store.get_level_k(Ej_idx, 0)
            Eofk = store.get_level_k(Ej_idx, level)
            energy = Eofk - E0
            std = np.std(energy[low_cut:])
            translated = (
                energy - energy[-1]
            )  # translate all last levels to the same height
            last_energy = energy[-1]
            e_label = f"{last_energy:.0f}" if last_energy >= 1 else f"{last_energy:.2E}"
            plt.plot(
                kk,
                translated,
                marker=".",
                label=f"E{level}={e_label}, $\sigma$=1e{np.log10(std):.0f}",
            )
            plt.legend()
            plt.axvline(x=kk[low_cut], color="r", linestyle="--")
            # plt.title(f"std=10^{np.log10(std):.0f}", fontsize=8)
            # plt.xlabel("k")
            # plt.ylabel(f"E{d}(k)-E0(k)")
        plt.title(f"Ej={Ej}")

    # plt.tight_layout(pad=0.7)  # Adjust the padding between plots
    # plt.subplots_adjust(top=0.85)  # Adjust the top to make space for suptitle
    plt.suptitle(
        f"Convergence of energy levels, dashed $\sigma$ cut at k={kk[low_cut]}. Each level is rel. to ground, then rel. final"
    )

    plt.show()
