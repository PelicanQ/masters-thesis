from matplotlib import pyplot as plt
from sim_store.store import Store
import numpy as np


# here we just line up all eigenvalues in increasing order
def level_lineup(
    store: Store, Ej_indices: list[int, int, int, int, int, int], k_idx: int
):
    Ejs = [store.Ejs[i] for i in Ej_indices]
    print(f"Lining up all energy levels for Ej {Ejs} at k={store.kk[k_idx]}")
    results = []
    for i, Ej_idx in enumerate(Ej_indices):
        levels = store.all_levels(Ej_idx=Ej_idx, k_idx=k_idx)
        results.append(levels - levels[0])
    grid_plot(
        results,
        Ejs,
        (2, 3),
        "n",
        "En",
        f"All energies, varying Ej, k={store.kk[k_idx]}",
        "Ej",
    )


def grid_plot(collection, params, shape, x, y, title, param_name):
    for i, vals in enumerate(collection):
        plt.subplot(shape[0], shape[1], i + 1)
        plt.plot(vals, marker=".")
        plt.ylabel(y)
        plt.xlabel(x)
        plt.title(f"{param_name}={params[i]}", fontsize=9)
    plt.suptitle(title)
    plt.show()
