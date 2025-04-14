# Let's make a Postgres storage system for sim data
from matplotlib import pyplot as plt
import numpy as np
from store.models import Levels2T, ZZ2T, ZZ3T, Levels3T
from functools import reduce
from operator import or_
from typing import Iterable

tol = 1e-6  # tolerance for search in float/double columns


class StoreLevels3T:
    all_keys = ["Ec2", "Ec3", "Ej1", "Ej2", "Ej3", "Eint12", "Eint23", "Eint13"]
    model = Levels3T
    max_level = 10

    @staticmethod
    def insert(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, levels):
        level_dict = dict([(f"E{i}", levels[i]) for i in range(len(levels))])
        return Levels2T.replace(
            Ec2=round(Ec2, 2),
            Ec3=round(Ec3, 2),
            Ej1=round(Ej1, 1),
            Ej2=round(Ej2, 1),
            Ej3=round(Ej3, 1),
            Eint12=round(Eint12, 2),
            Eint23=round(Eint23, 2),
            Eint13=round(Eint13, 2),
            **level_dict,
        ).execute()

    @classmethod
    def line(cls, **kwargs):
        missing_key, query = get_missing_key(kwargs, cls)
        vars = []
        levels = np.zeros((len(query), cls.max_level + 1))

        for i, entry in enumerate(query):
            vars.append(getattr(entry, missing_key))
            for j in range(cls.max_level + 1):
                levels[i, j] = getattr(entry, f"E{j}")
        if len(vars) < 1:
            raise Exception("It seems given values were not found")
        return vars, levels


class StoreLevels2T:
    all_keys = ["Ec2", "Ej1", "Ej2", "Eint"]
    model = Levels2T
    max_level = 7

    @staticmethod
    def insert(Ec2, Ej1, Ej2, Eint, levels):
        level_dict = dict([(f"E{i}", levels[i]) for i in range(len(levels))])
        return Levels2T.replace(
            Ec2=round(Ec2, 2), Ej1=round(Ej1, 1), Ej2=round(Ej2), Eint=round(Eint, 2), **level_dict
        ).execute()

    @staticmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            cls.insert(res["Ec2"], res["Ej1"], res["Ej2"], res["Eint"], res["levels"])

    @classmethod
    def line(cls, **kwargs):
        missing_key, query = get_missing_key(kwargs, cls)
        vars = []
        levels = np.zeros((len(query), cls.max_level + 1))

        for i, entry in enumerate(query):
            vars.append(getattr(entry, missing_key))
            for j in range(cls.max_level + 1):
                levels[i, j] = getattr(entry, f"E{j}")
        if len(vars) < 1:
            raise Exception("It seems given values were not found")
        return vars, levels

    @classmethod
    def meshline(cls, **kwargs):
        # query along a one dimensional mesh. Exception is raised upon missing values
        levels = np.zeros((len(query), cls.max_level + 1))
        query = meshline_query(cls, kwargs)
        for i, entry in enumerate(query):
            for j in range(cls.max_level + 1):
                levels[i, j] = getattr(entry, f"E{j}")
        return levels  # along a column is a certain energy level vs the iterable

    @classmethod
    def plane(cls, var1: str, val1: Iterable, var2: str, val2: Iterable, **kwargs):
        """Make a meshline over var2 then repeat for different var1.
        Note: the iterables are assumed to be in increasing order"""

        kwargs[var2] = val2
        # all thesea are gale shapely
        level_planes = [np.zeros((len(val2), len(val1))) for _ in range(cls.max_level + 1)]
        for i, val in enumerate(val1):
            kwargs[var1] = val
            energies = cls.meshline(**kwargs)  # a line as function of var2
            for j in range(energies.shape[1]):
                level_planes[j][:, i] = energies[:, j]
        return level_planes


class Store_zz3T:
    all_keys = ["Ec2", "Ec3", "Ej1", "Ej2", "Ej3", "Eint12", "Eint23", "Eint13"]
    all_vals = ["zzGS12", "zzGS23", "zzGS13", "zzzGS"]
    model = ZZ3T

    @classmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            fields = [(field, res[field]) for field in (cls.all_keys + cls.all_vals)]
            # this selection excludes k. We don't insert k
            cls.insert(**dict(fields))

    @staticmethod
    def insert(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, zzGS12, zzGS23, zzGS13, zzzGS, k=None):
        # accept k parameter but ignore
        return ZZ3T.replace(
            Ec2=round(Ec2, 2),
            Ec3=round(Ec3, 2),
            Ej1=round(Ej1, 1),
            Ej2=round(Ej2, 1),
            Ej3=round(Ej3, 1),
            Eint12=round(Eint12, 2),
            Eint23=round(Eint23, 2),
            Eint13=round(Eint13, 2),
            zzGS12=zzGS12,
            zzGS23=zzGS23,
            zzGS13=zzGS13,
            zzzGS=zzzGS,
        ).execute()

    @classmethod
    def get_all(cls):
        results = {key: [] for key in cls.all_vals}
        query = cls.model.select()
        for entry in query:
            for column in cls.all_vals:
                results[column].append(getattr(entry, column))

        return (results["zzGS12"], results["zzGS23"], results["zzGS13"], results["zzzGS"])

    @classmethod
    def line(cls, **kwargs):
        missing_key, query = get_missing_key(kwargs, cls)
        vars = []
        results = {key: [] for key in cls.all_vals}
        for entry in query:
            vars.append(getattr(entry, missing_key))
            for column in cls.all_vals:
                results[column].append(getattr(entry, column))
        if len(vars) < 1:
            raise Exception("It seems given values were not found")
        return vars, *(results[val] for val in cls.all_vals)

    @classmethod
    def meshline(cls, **kwargs):
        # query along a one dimensional mesh. Exception is raised upon missing values
        query = meshline_query(cls, kwargs)
        results = {key: [] for key in cls.all_vals}
        for entry in query:
            for column in cls.all_vals:
                results[column].append(getattr(entry, column))
        return (results["zzGS12"], results["zzGS23"], results["zzGS13"], results["zzzGS"])

    @classmethod
    def plane(cls, var1: str, val1: Iterable, var2: str, val2: Iterable, **kwargs):
        # make a meshline over var2 then repeat for different var1
        kwargs[var2] = val2
        # all thesea are gale shapely
        zz12 = np.zeros((len(val2), len(val1)))
        zz23 = np.zeros((len(val2), len(val1)))
        zz13 = np.zeros((len(val2), len(val1)))
        zzz = np.zeros((len(val2), len(val1)))
        zz12[:] = np.nan
        zz23[:] = np.nan
        zz13[:] = np.nan
        zzz[:] = np.nan
        for i, val in enumerate(val1):
            kwargs[var1] = val
            zz12_line, zz23_line, zz13_line, zzz_line = cls.meshline(**kwargs)  # a line as function of var2
            zz12[:, i] = zz12_line
            zz23[:, i] = zz23_line
            zz13[:, i] = zz13_line
            zzz[:, i] = zzz_line
        return zz12, zz23, zz13, zzz


class Store_zz2T:
    all_keys = ["Ec2", "Ej1", "Ej2", "Eint"]
    all_vals = ["zz", "zzGS"]
    model = ZZ2T

    @classmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            cls.insert(res["Ec2"], res["Ej1"], res["Ej2"], res["Eint"], res["zz"], res["zzGS"])

    @staticmethod
    def insert(Ec2, Ej1, Ej2, Eint, zz, zzGS):
        return ZZ2T.replace(
            Ec2=round(Ec2, 2), Ej1=round(Ej1, 1), Ej2=round(Ej2), Eint=round(Eint, 2), zz=zz, zzGS=zzGS
        ).execute()

    @classmethod
    def line(cls, **kwargs):
        missing_key, query = get_missing_key(kwargs, cls)
        vars = []
        zz = []
        zzGS = []
        for entry in query:
            vars.append(getattr(entry, missing_key))
            zz.append(entry.zz)
            zzGS.append(entry.zzGS)
        if len(vars) < 1:
            raise Exception("It seems given values were not found")
        return vars, zz, zzGS

    @classmethod
    def meshline(cls, **kwargs):
        # query along a one dimensional mesh. Exception is raised upon missing values
        query = meshline_query(cls, kwargs)
        zz = []
        zzGS = []
        for entry in query:
            zz.append(entry.zz)
            zzGS.append(entry.zzGS)
        return zz, zzGS

    @classmethod
    def plane(cls, var1: str, val1, var2: str, val2, **kwargs):
        # repeated var2 meshlines
        kwargs[var2] = val2  # this enters meshline as the sweep
        zzplane = np.zeros((len(val2), len(val1)))
        zzGSplane = np.zeros((len(val2), len(val1)))
        zzplane[:] = np.nan
        zzGSplane[:] = np.nan
        for i, val in enumerate(val1):
            kwargs[var1] = val
            zz, zzGS = cls.meshline(**kwargs)  # a line as function of var2
            zzplane[:, i] = zz
            zzGSplane[:, i] = zzGS
        return zzplane, zzGSplane


def approx_in(field, values):
    conditions = [field.between(v - tol, v + tol) for v in values]
    return reduce(or_, conditions)


def meshline_query(cls, kwargs):
    # the idea is that one of kwargs is an iterable and we return entries with those values in ascending order
    iterable = get_iterable_key(kwargs)
    query = cls.model.select()
    for key, val in kwargs.items():
        # the fixed ones
        if key != iterable:
            query = query.where(getattr(cls.model, key).between(val - tol, val + tol))
    query = query.where(approx_in(getattr(cls.model, iterable), kwargs[iterable]))
    query = query.order_by(getattr(cls.model, iterable))
    if len(query) != len(kwargs[iterable]):
        raise Exception("Requested variables could not be found")
    return query


def get_missing_key(kwargs, cls):
    keys = kwargs.keys()
    missing_keys = list(filter(lambda s: s not in keys, cls.all_keys))
    if len(missing_keys) != 1:
        raise Exception("One key must be undefined")
    missing_key = missing_keys[0]
    print("variable: ", missing_key)

    query = cls.model.select()
    for key, val in kwargs.items():
        query = query.where(getattr(cls.model, key).between(val - tol, val + tol))
    return missing_key, query


def get_iterable_key(kwargs: dict) -> str:
    # intended for when one key is iterable
    iterable_name: str = None
    for key, val in kwargs.items():
        try:
            iter(val)
            iterable = True
        except:
            iterable = False
        if iterable:
            iterable_name = key
    if iterable_name == None:
        raise Exception("Failed to find")
    return iterable_name


def view():
    Ej2 = 50
    Eint = 0.1
    Ec2 = 1
    q = ZZ2T.select().where(ZZ2T.Eint == Eint).where(ZZ2T.Ec2 == Ec2)
    Ej1s = []
    Ej2s = []
    zzGS = []
    for entry in q:
        print(entry.Ej1, entry.Ej2)
        Ej1s.append(entry.Ej1)
        Ej2s.append(entry.Ej2)
        zzGS.append(entry.zzGS)
    X = np.array([[0, 1, 3], [0, 1, 2]])
    Y = np.array([[0, 0, 0], [1, 1, 1]])
    C = np.array([[1, 2, 3], [4, 5, 6]])
    plt.pcolormesh(X, Y, C, shading="nearest")
    plt.show()


if __name__ == "__main__":
    x = np.arange(0, 0.9, 0.05)
    y = np.arange(30, 70, 2)
    vars, zz, zzGS = Store_zz2T.line(Eint=0.1, Ej1=50, Ej2=50)
    print(vars)
    plt.plot(vars, zzGS)
    plt.show()

    pass
