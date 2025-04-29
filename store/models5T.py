from peewee import Model, DoubleField, CompositeKey
from store.db import db


class ZZ5T_triang(Model):
    # All Ec = 1
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Ej3 = DoubleField()
    Ej4 = DoubleField()
    Ej5 = DoubleField()

    Eint12 = DoubleField()
    Eint23 = DoubleField()
    Eint13 = DoubleField()
    Eint34 = DoubleField()
    Eint45 = DoubleField()
    Eint35 = DoubleField()

    zz13 = DoubleField()
    zz35 = DoubleField()
    zz15 = DoubleField()
    zzz135 = DoubleField()

    class Meta:
        database = db
        strict_tables = True
        primary_key = CompositeKey(
            "Ej1", "Ej2", "Ej3", "Ej4", "Ej5", "Eint12", "Eint23", "Eint13", "Eint34", "Eint45", "Eint35"
        )
