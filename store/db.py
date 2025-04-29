from peewee import SqliteDatabase

db = SqliteDatabase(
    "db.db",
    pragmas={"foreign_keys": 1},  # Enforce foreign-key constraints
)
