from matplotlib import pyplot as plt
import numpy as np
from matplotlib import colors


def OrBu_colormap():
    # First, sample 20 points from the Blues colormap in reverse order
    colors1 = plt.cm.Blues_r(np.linspace(0.0, 1, 20))
    # Then, sample 20 points from the Oranges colormap
    colors2 = plt.cm.Oranges(np.linspace(0.0, 0.8, 20))
    # If you want to have less white, you can increase the 0 (e.g., to 0.1 in both cases -- I recommend doing it symmetrically)
    # If you want the Blues or the Oranges to not get so dark, decrease the 1 (I personally prefer around 0.9 in the Oranges, it's a bit softer)
    # Now, concatenate the maps into one discrete map of 40 colors
    colorss = np.vstack((colors1, colors2))
    # Finally, create a continuous map from the discrete one
    mymap = colors.LinearSegmentedColormap.from_list("my_colormap", colorss)
    return mymap
