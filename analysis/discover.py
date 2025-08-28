import numpy as np
from matplotlib import pyplot as plt
import functools
from matplotlib.widgets import Slider
from sandbox.util import make_axslid, makeline, makeslid


def format_coord(X, Y, getZ, x, y):
    # print(X)
    xarr = X[0, :]
    yarr = Y[:, 0]
    if (x > xarr.min()) & (x <= xarr.max()) & (y > yarr.min()) & (y <= yarr.max()):
        col = np.searchsorted(xarr, x) - 1
        row = np.searchsorted(yarr, y) - 1
        z = getZ()[row, col]
        return f"x={x:.2E}, y={y:.2E}, z={z:.2E}   [{row},{col}]"
    else:
        return f"x={x:1.5f}, y={y:1.5f}"


def make_format_coord(X, Y, Z):
    return functools.partial(format_coord, X, Y, lambda: Z)


def make_format_coord_refreshable(X, Y, vals, key):
    return functools.partial(format_coord, X, Y, lambda: vals[key])


def make_mesh(X, Y, Z, format_coord, norm=None, cmap=None, ax=None):
    if ax:
        c = ax.pcolormesh(X, Y, Z, norm=norm, cmap=cmap)
        ax.format_coord = format_coord
        return c
    fig, ax = plt.subplots()
    c = ax.pcolormesh(X, Y, Z, norm=norm, cmap=cmap)
    ax.format_coord = format_coord
    cbar = fig.colorbar(c)
    return fig, ax, c, cbar


def make_hoverax_refreshable(X, Y, vals: dict, key: str, norm, cmap, ax=None):
    """Improvement of make_hoverax where a dict supplies values so that hover shows updated values"""
    format_coord = make_format_coord_refreshable(X, Y, vals, key)
    return make_mesh(X, Y, vals[key], format_coord, norm=norm, cmap=cmap, ax=ax)


def make_hoverax(X, Y, Z, norm=None, cmap=None, ax=None):
    """In addtion to x,y with this you see z value when hovering"""
    return make_mesh(X, Y, Z, make_format_coord(X, Y, Z), norm=norm, cmap=cmap, ax=ax)


def is_cross_coupling(arg: str):
    if arg[0] != "g":
        return False
    if (int(arg[2]) - int(arg[1])) == 1:
        return False
    return True


def make_discover(args: list[str], inits: list[float], X, Y, calculate, norm, cmap=None):
    fig_ctl = plt.figure()
    fig_ctl.suptitle("Controls")
    y = 0.9
    slids: dict[str, Slider] = {}
    globals()[
        str(np.random.randint(1e5, 1e8))
    ] = slids  # if a global reference is not kept, Sliders become unresponsive
    for arg, init in zip(args, inits):
        axslid = make_axslid(0.15, y, fig_ctl, 0.75)
        if arg[0] == "g":
            slid = makeslid(
                axslid,
                arg,
                0,
                0.0001 if is_cross_coupling(arg) else 0.01,
                0.01 if is_cross_coupling(arg) else 0.5,
                init,
            )
        elif arg[0] == "d":
            slid = makeslid(axslid, arg, 0, 0.05, 10, init)
        elif arg[0] == "a":
            slid = makeslid(axslid, arg, -2, 0.01, 1.8, init)
        else:
            raise Exception("This is not a g or delta")
        slids[arg] = slid
        y -= 0.1

    initval = calculate(**dict(zip(args, inits))) * np.nan
    val_dict = {"val": initval}
    fig, ax, c, cbar = make_hoverax_refreshable(X, Y, val_dict, "val", norm=norm, cmap=cmap)

    def update(val):
        kwargs = {}
        for key, slid in slids.items():
            kwargs[key] = slid.val
        val_mat = calculate(**kwargs)

        c.set_array(val_mat)
        val_dict["val"] = val_mat
        fig.canvas.draw_idle()

    update(0)
    for s in slids.values():
        s.on_changed(update)
    return ax
