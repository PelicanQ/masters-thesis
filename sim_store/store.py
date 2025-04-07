import numpy as np
import pandas as pd

# the csv file is the source of truth for the Ej and k grid
# kk = np.concatenate(
#     [
#         np.arange(start=6, stop=20, step=1),
#         np.arange(start=20, stop=40, step=3),
#         np.arange(start=40, stop=70, step=5),
#     ]
# )
# Ejs = np.concatenate(
#     [
#         np.arange(start=1, stop=10, step=1),
#         np.arange(start=10, stop=40, step=5),
#         np.arange(start=40, stop=100, step=10),
#         np.arange(start=100, stop=500, step=50),
#         np.arange(start=500, stop=1000, step=80),
#     ]
# )


class Store:
    def __init__(self, store_file: str, keys_file: str, *, calc_dim=None):
        # keys is the file name to csv with the Ej and k grid
        # This grid is fixed
        # calc_dim returns total matrix size given k

        keys = pd.read_csv(keys_file, header=None, index_col=None).to_numpy()
        Ejs = keys[0]
        Ejs = Ejs[~np.isnan(Ejs)].astype(int)

        kk = keys[1]
        kk = kk[~np.isnan(kk)].astype(int)

        self.Ejs = Ejs
        self.kk = kk
        print(f"Init store with kk={kk} Ejs={Ejs}")
        try:
            np.load(store_file)
        except FileNotFoundError:
            if len(keys) == 2:
                # keys files does not specify third dim length. calc_dim should be given
                maxK = np.max(kk)
                num_energies = calc_dim(maxK)
            else:
                num_energies = int(keys[2][0])

            d = np.empty(shape=(len(Ejs), len(kk), num_energies))
            d[:] = np.nan
            print("created store, shape", d.shape)
            np.save(store_file, d)

        self.name = store_file
        self.notnan()

    def notnan(self):
        d = np.load(self.name)
        num_defined = np.sum(~np.isnan(d).all(axis=2))
        total = len(self.kk) * len(self.Ejs)
        print(
            f"Number of input points defined: {num_defined}/{total}",
        )

    def shape(self):
        d = np.load(self.name)
        return d.shape

    def save_levels(self, Ej_idx, k_idx, vals):
        d = np.load(self.name)
        d[Ej_idx, k_idx, :] = vals
        np.save(self.name, d)

    def clear(self):
        # does not remove file but replaces all values with nan
        d = np.load(self.name)
        d[:] = np.nan
        np.save(self.name, d)

    def get_level_Ej(self, k_idx, n):
        d = np.load(self.name)
        return d[:, k_idx, n]

    def get_level_k(self, Ej_idx, n):
        d = np.load(self.name)
        return d[Ej_idx, :, n]

    def all_levels(self, Ej_idx, k_idx):
        d = np.load(self.name)
        return d[Ej_idx, k_idx, :]
