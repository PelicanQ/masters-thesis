import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def make_axslid(x, y):
    sliderwidth = 0.35
    return plt.axes([x, y, sliderwidth, 0.03])


def makeslid(ax_slid, name, init, step, space: int = 2):
    return Slider(ax_slid, name, init - space, init + space, valinit=init, valstep=step)


def makeline(height, col, state: str, bare: bool = False):
    return plt.plot(
        [-1, 1],
        [height, height],
        lw=2,
        color=col,
        linestyle=":" if bare else "-",
        marker="o" if bare else "",
        label=state,
    )
