from matplotlib import pyplot as plt
import numpy as np
from ..store import Store


# this uses a Store
def E0(store: Store, Ej_indices: list[int, int, int, int]):
    # Zero level convergence for four Ejs
    # check length compatible
    Ejlen = store.shape()[2]
    maxi = max(Ej_indices)
    if maxi >= Ejlen:
        raise Exception(f"Max of Ej indices {maxi}, Ej length {Ejlen}")

    kk = store.kk
    Ejs = store.Ejs

    print("Checking ground level for Ej ", [Ejs[i] for i in Ej_indices])

    low_cut = 5  # lower cut for std
    plt.figure(figsize=(12, 6))

    # now make a subplot for each energy level relative to lowest
    for i, Ej_idx in enumerate(Ej_indices):
        plt.subplot(2, 2, i + 1)
        Ej = Ejs[Ej_idx]
        E0 = store.get_level_k(Ej_idx, 0)
        std = np.std(E0[low_cut:])
        plt.plot(kk, E0, marker=".")
        plt.axvline(x=kk[low_cut], color="r", linestyle="--")
        plt.title(f"Ej={Ej} std=10^{np.log10(std):.0f}", fontsize=9)
        plt.xlabel("k")
        plt.ylabel(f"E0(k)")
        # plt.tight_layout(pad=0.7)  # Adjust the padding between plots

    # plt.subplots_adjust(top=0.85)  # Adjust the top to make space for suptitle
    plt.suptitle(f"Convergence of ground level for varying Ej, dashed low_cut at k={kk[low_cut]}")

    plt.show()
