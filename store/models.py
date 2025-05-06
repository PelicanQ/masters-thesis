# Let's make a Postgres storage system for sim data
from peewee import Model, DoubleField, CompositeKey, SqliteDatabase
from store.models5T import ZZ5T_triang
from store.models4T import ZZ4T
from store.db import db


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


if __name__ == "__main__":
    db.create_tables([ZZ4T])
    pass
