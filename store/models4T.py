from peewee import Model, DoubleField, CompositeKey, SqliteDatabase


class ZZ4T(Model):
    # All Ec = 1
    # Some couplings
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Ej3 = DoubleField()
    Ej4 = DoubleField()
    Eint12 = DoubleField()
    Eint23 = DoubleField()
    Eint34 = DoubleField()
    Eint14 = DoubleField()

    zz12 = DoubleField()
    zz13 = DoubleField()
    zz14 = DoubleField()
    zz23 = DoubleField()
    zz24 = DoubleField()
    zz34 = DoubleField()

    zzz123 = DoubleField()
    zzz124 = DoubleField()
    zzz134 = DoubleField()
    zzz234 = DoubleField()

    zzzz = DoubleField()
