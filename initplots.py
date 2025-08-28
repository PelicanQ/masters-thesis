# Import to activate SciencePlots and set the font-sizes
from matplotlib import pyplot as plt
import scienceplots

plt.style.use(["science", "nature"])
# plt.rcParams.update(
#     {
#         "font.size": 11,
#         "axes.labelsize": 11,
#         "axes.titlesize": 11,
#         "xtick.labelsize": 10,
#         "ytick.labelsize": 10,
#         "legend.fontsize": 11,
#     }
# )

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 10,
    }
)
