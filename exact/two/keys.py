import numpy as np
import pandas as pd
from hamil import calc_eig

# this files generates the input space grid
kk = np.concatenate(
    [
        np.arange(start=5, stop=12, step=2),
        np.arange(start=12, stop=20, step=3),
        np.arange(start=20, stop=40, step=4),
    ]
)
Ej = np.concatenate([[1, 5, 10, 50, 100, 500, 1000]])
print("kk len", len(kk), "Ej len", len(Ej))
num_energies = 50
df = pd.DataFrame((Ej, kk, [num_energies]))

df.to_csv("keys_grid.csv", index=False, header=False)
