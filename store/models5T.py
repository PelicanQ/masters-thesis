from peewee import Model, DoubleField, CompositeKey


class ZZ5T(Model):
    # All Ec = 1
    # Some couplings
    Ej1 = DoubleField()
    Ej2 = DoubleField()
    Ej3 = DoubleField()
    Ej4 = DoubleField()
    Ej5 = DoubleField()
    # bit1
    Eint12 = DoubleField()
    Eint13 = DoubleField()
    # bit2
    Eint23 = DoubleField()
    # bit3
    Eint34 = DoubleField()
    Eint35 = DoubleField()
    # bit4
    Eint45 = DoubleField()

    zz13 = DoubleField()
    zz35 = DoubleField()
    zzz135 = DoubleField()
