from store.models import ZZ3T
from store.stores import Store_zz3T
from peewee import SqliteDatabase

# After collecting data in a SQLite db local to the remote machine, here it can be merged into existing
# Target database will be the one on the machine running this file
# Source database
source = SqliteDatabase(
    "remotedata.db",
    pragmas={"foreign_keys": 1},  # Enforce foreign-key constraints
)

rows = []
with ZZ3T.bind_ctx(source):
    query = ZZ3T.select()
    for row in query:
        rows.append(row)

all_columns = Store_zz3T.all_keys + Store_zz3T.all_vals

for i, row in enumerate(rows):
    print(i)
    d = dict([(col, getattr(row, col)) for col in all_columns])
    ZZ3T.replace(**d).execute()
