from store.models5T import ZZ5T_triang
from store.models4T import ZZ4T
from store.stores5T import Store_zz5T_triang
from store.stores4T import Store_zz4T
from peewee import SqliteDatabase

# After collecting data in a SQLite db local to the remote machine, here it can be merged into existing
# Target database will be the one on the machine running this file
# Source database
source = SqliteDatabase(
    "remotedata.db",
    pragmas={"foreign_keys": 1},  # Enforce foreign-key constraints
)
if __name__ == "__main__":
    rows = []
    with ZZ4T.bind_ctx(source):
        query = ZZ4T.select()
        for row in query:
            rows.append(row)

    all_columns = Store_zz4T.all_keys + Store_zz4T.all_vals

    for i, row in enumerate(rows):
        print(i)
        d = dict([(col, getattr(row, col)) for col in all_columns])
        ZZ4T.replace(**d).execute()
