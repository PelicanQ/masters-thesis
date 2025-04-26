import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.axes import Axes


def make_axslid(x, y, fig=None, sliderwidth=0.35):
    if fig:
        return fig.add_axes([x, y, sliderwidth, 0.03])
    return plt.axes([x, y, sliderwidth, 0.03])


def makeslid(ax_slid: Axes, name, mid, step, space: int = 2, init=None):
    slider = Slider(ax_slid, name, mid - space, mid + space, valinit=init or mid, valstep=step)
    ax_slid.plot([0, 0], [0, 1])
    return slider


def makeline(height, col, state: str, bare: bool = False, ax=None):
    obj = ax if ax else plt
    return obj.plot(
        [-1, 1],
        [height, height],
        lw=2,
        color=col,
        linestyle=":" if bare else "-",
        marker="o" if bare else "",
        label=state,
    )
