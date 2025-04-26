from pathlib import Path
from analysis import ground, conv, levels
from sim_store.store import Store

# Zero level convergence
fstore = (Path(__file__).parent / "store2.npy").resolve()
fkeys = (Path(__file__).parent / "keys_grid.csv").resolve()

store = Store(fstore, fkeys)

# Ground level
Ej_indices = [0, 2, 5, 6]
# ground.E0(store, Ej_indices)

# Other levels
Ej_indicies = [0, 2, 5, 6]
energy_levels = [1, 3, 20, 40]
# conv.conv(store, energy_levels, Ej_indicies)

Ej_indicies = [0, 2, 3, 4, 5, 6]
levels.level_lineup(store, Ej_indicies, 11)
