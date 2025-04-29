from peewee import Model, DoubleField, CompositeKey
from store.db import db


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
