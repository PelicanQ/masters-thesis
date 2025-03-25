from pathlib import Path
from sim_store.store import Store
from .hamil import calc_eig
import time

# Collection of data
# Run with different Eint
fstore = (Path(__file__).parent / "store2.npy").resolve()
fkeys = (Path(__file__).parent / "keys_grid.csv").resolve()
store = Store(fstore, fkeys)

n_vals = store.shape()[2]  # energy dimension length
print("nvals", n_vals)
Ejs = store.Ejs
kk = store.kk  # 5 sec to sweep kk for one Ej

print("k:", store.kk)
print("Ej:", store.Ejs)
start_time = time.time()
for j, Ej in enumerate(Ejs):
    for k_idx, k in enumerate(kk):
        vals = calc_eig(Ej=Ejs[j], Eint=2, k=k)
        store.save_levels(j, k_idx, vals[:n_vals])
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
