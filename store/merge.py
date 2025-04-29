from store.models5T import ZZ5T_triang
from store.stores5T import Store_zz5T_triang
from peewee import SqliteDatabase

# After collecting data in a SQLite db local to the remote machine, here it can be merged into existing
# Target database will be the one on the machine running this file
# Source database
source = SqliteDatabase(
    "remote.db",
    pragmas={"foreign_keys": 1},  # Enforce foreign-key constraints
)
if __name__ == "__main__":
    rows = []
    with ZZ5T_triang.bind_ctx(source):
        query = ZZ5T_triang.select()
        for row in query:
            rows.append(row)

    all_columns = Store_zz5T_triang.all_keys + Store_zz5T_triang.all_vals

    for i, row in enumerate(rows):
        print(i)
        d = dict([(col, getattr(row, col)) for col in all_columns])
        ZZ5T_triang.replace(**d).execute()
