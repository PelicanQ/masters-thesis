# recreate figure 6 in ZZ paper
from other.colormap import OrBu_colormap
import numpy as np
from matplotlib import pyplot as plt
from anharm.Hamiltonian import Hamil
from matplotlib import colors
import inspect
from analysis.discover import make_hoverax_refreshable, make_hoverax, make_mesh
from sandbox.util import make_axslid, makeline, makeslid
from matplotlib.widgets import Slider


def getextrazz13(H: Hamil):
    space1 = H.get_subspace(1)
    space2 = H.get_subspace(2)
    extra1000 = space1.get_second_edge("1000", "0001", False) + space1.get_leg("1000", "0010", "0001")
    extra0010 = (
        space1.get_bird("0010", "0001", "1000")
        + space1.get_bird("0010", "0001", "0100")
        + space1.get_edge("0010", "0001")
    )
    extra1 = extra1000 + extra0010

    four = space2.get_4loop_contraction("1010", "0011")
    edge = space2.get_edge("1010", "1001")
    nn = ["0020", "1100", "2000"]  # neighbors for birds
    birds = sum([space2.get_bird("1010", "1001", n) for n in nn])
    extra2 = four + edge + birds
    extrazz = extra2 - extra1
    return extrazz
