from store.models3T import ZZ3T
from store.models5T import ZZ5T_triang
from store.models4T import ZZ4T
from store.stores5T import Store_zz5T_triang
from store.stores4T import Store_zz4T
from store.stores3T import Store_zz3T
from peewee import SqliteDatabase
import numpy as np

# After collecting data in a SQLite db local to the remote machine, here it can be merged into existing
# Target database will be the one on the machine running this file
# Source database
source = SqliteDatabase(
    "rem.db",
    pragmas={"foreign_keys": 1},  # Enforce foreign-key constraints
)
if __name__ == "__main__":
    rows = []
    with ZZ3T.bind_ctx(source):
        query = ZZ3T.select().where(
            ZZ3T.Eint12 == 0.04 and ZZ3T.Eint23 == 0.04 and ZZ3T.Ej3 == 50 and ZZ3T.Eint13 == 0.0013
        )
        # print(len(query))
        for row in query:
            rows.append(row)
    all_columns = Store_zz3T.all_keys + Store_zz3T.all_vals
    # Ej1s = np.arange(30, 100, 0.2)
    # Ej2s = np.arange(30, 140, 0.2)
    for i, row in enumerate(rows):
        print(i)
        d = dict([(col, getattr(row, col)) for col in all_columns])
        ZZ3T.replace(**d).execute()
