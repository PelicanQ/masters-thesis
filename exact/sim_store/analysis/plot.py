from matplotlib import pyplot as plt
import numpy as np


def num2shape(num):
    match num:
        case 2:
            return (1, 2)
        case 3:
            return (1, 3)
        case 4:
            return (2, 2)
        case 6:
            return (2, 3)


def grid_plot2d(
    xx,
    collection: np.ndarray,
    params,
    xlabel: str,
    ylabel: str,
    suptitle: str,
    param_name: str,
    marker=None,
    *,
    std: None | int = None,
):
    shape = num2shape(collection.shape[0])
    for i in range(collection.shape[0]):
        plt.subplot(shape[0], shape[1], i + 1)
        y = collection[i, :]
        plt.plot(xx, y, marker=marker)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        title = f"{param_name}={params[i]}"
        if std is not None:
            plt.axvline(x=xx[std], color="r", linestyle="--")
            dev = np.std(y[std:])
            title += f", std=1e{np.log10(dev):.0f}"
        plt.title(title, fontsize=9)
    plt.suptitle(suptitle)
    plt.show()


def grid3d(
    xx,
    collection: list[np.ndarray],
    params,
    xlabel: str,
    ylabel: str,
    labels: list[str],
    param_name: str,
    suptitle: str,
    marker=None,
    std: None | int = None,
):
    # each array of collection will be row indexed with level_select
    plt.figure(figsize=(12, 6))
    shape = num2shape(len(collection))
    for i, levels in enumerate(collection):
        plt.subplot(shape[0], shape[1], i + 1)
        # handle one plot.
        for a in range(levels.shape[0]):
            y = levels[a, :]
            label = labels[a]
            if std:
                devi = np.std(y[std:])
                label += f", $\sigma$=1e{np.log10(devi):.0f}"
            plt.plot(xx, y, marker=marker, label=label)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(f"{param_name}={params[i]}", fontsize=9)
        plt.legend()

    plt.suptitle(suptitle)
    plt.show()
