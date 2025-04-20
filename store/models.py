# Let's make a Postgres storage system for sim data
from peewee import Model, DoubleField, CompositeKey, SqliteDatabase


db = SqliteDatabase(
    "db.db",
    pragmas={"foreign_keys": 1},  # Enforce foreign-key constraints
)


class Levels2T(Model):
    Ec2 = DoubleField()
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Eint = DoubleField()
    E0 = DoubleField()
    E1 = DoubleField()
    E2 = DoubleField()
    E3 = DoubleField()
    E4 = DoubleField()
    E5 = DoubleField()
    E6 = DoubleField()
    E7 = DoubleField()

    class Meta:
        database = db
        strict_tables = True
        primary_key = CompositeKey("Ec2", "Ej1", "Ej2", "Eint")


class ZZ2T(Model):
    Ec2 = DoubleField()
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Eint = DoubleField()
    zz = DoubleField()
    zzGS = DoubleField()

    class Meta:
        database = db
        strict_tables = True
        primary_key = CompositeKey("Ec2", "Ej1", "Ej2", "Eint")


class Levels3T(Model):
    Ec2 = DoubleField()
    Ec3 = DoubleField()
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Ej3 = DoubleField()
    Eint12 = DoubleField()
    Eint23 = DoubleField()
    Eint13 = DoubleField()

    E0 = DoubleField()
    E1 = DoubleField()
    E2 = DoubleField()
    E3 = DoubleField()
    E4 = DoubleField()
    E5 = DoubleField()
    E6 = DoubleField()
    E7 = DoubleField()
    E8 = DoubleField()
    E9 = DoubleField()
    E10 = DoubleField()

    class Meta:
        database = db
        strict_tables = True
        primary_key = CompositeKey("Ec2", "Ec3", "Ej1", "Ej2", "Ej3", "Eint12", "Eint23", "Eint13")


class ZZ3T(Model):
    Ec2 = DoubleField()
    Ec3 = DoubleField()
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Ej3 = DoubleField()
    Eint12 = DoubleField()
    Eint23 = DoubleField()
    Eint13 = DoubleField()

    zzGS12 = DoubleField()
    zzGS23 = DoubleField()
    zzGS13 = DoubleField()
    zzzGS = DoubleField()

    class Meta:
        database = db
        strict_tables = True
        primary_key = CompositeKey("Ec2", "Ec3", "Ej1", "Ej2", "Ej3", "Eint12", "Eint23", "Eint13")


if __name__ == "__main__":
    pass
