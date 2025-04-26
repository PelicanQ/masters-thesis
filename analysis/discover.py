import numpy as np
from matplotlib import pyplot as plt
import functools


def format_coord(X, Y, getZ, x, y):
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


def make_mesh(X, Y, Z, norm, cmap, format_coord, ax=None):
    if ax:
        c = ax.pcolormesh(X, Y, Z, norm=norm, cmap=cmap)
        ax.format_coord = format_coord
        return c
    fig, ax = plt.subplots()
    c = ax.pcolormesh(X, Y, Z, norm=norm, cmap=cmap)
    ax.format_coord = format_coord
    fig.colorbar(c)


def make_hoverax_refreshable(X, Y, vals: dict, key: str, norm, cmap, ax=None):
    """Improvement of make_hoverax where a dict supplies values so that hover shows updated values"""
    format_coord = make_format_coord_refreshable(X, Y, vals, key)
    return make_mesh(X, Y, vals[key], norm, cmap, format_coord, ax=ax)


def make_hoverax(X, Y, Z, norm, cmap, ax=None):
    """In addtion to x,y with this you see z value when hovering"""
    return make_mesh(X, Y, Z, norm, cmap, make_format_coord(X, Y, Z), ax=ax)
