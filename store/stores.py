# Let's make a Postgres storage system for sim data
from matplotlib import pyplot as plt
import numpy as np
from store.models import Levels2T, ZZ2T
from typing import Iterable
from store.util import filter_grid, meshline_query, get_missing_key, get_where_query, line_query


class StoreLevels2T:
    all_keys = ["Ec2", "Ej1", "Ej2", "Eint"]
    model = Levels2T
    max_level = 7

    @staticmethod
    def insert(Ec2, Ej1, Ej2, Eint, levels):
        level_dict = dict([(f"E{i}", levels[i]) for i in range(len(levels))])
        return Levels2T.replace(
            Ec2=round(Ec2, 2), Ej1=round(Ej1, 1), Ej2=round(Ej2, 1), Eint=round(Eint, 2), **level_dict
        ).execute()

    @classmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            cls.insert(res["Ec2"], res["Ej1"], res["Ej2"], res["Eint"], res["levels"])

    @classmethod
    def line(cls, **kwargs):
        missing_key = get_missing_key(kwargs, cls)
        query = get_where_query(cls, kwargs)
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
        query = meshline_query(cls, kwargs)
        levels = np.zeros((len(query), cls.max_level + 1))
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


class StoreBase:
    @classmethod
    def check_exists(cls, **kwargs):
        """To avoid duplicate work, use this to see if data already exists"""
        keys = list(filter(lambda key: key in cls.all_keys, kwargs.keys()))
        if len(keys) != len(cls.all_keys):
            raise Exception("Please supply all keys")
        query = get_where_query(cls, dict([(key, kwargs[key]) for key in keys]))
        # in case some float rounding artifact has inserted what we consider duplicates
        return query.count() >= 1


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
            Ec2=round(Ec2, 2), Ej1=round(Ej1, 1), Ej2=round(Ej2, 1), Eint=round(Eint, 2), zz=zz, zzGS=zzGS
        ).execute()

    @classmethod
    def line(cls, **kwargs):
        missing_key = get_missing_key(kwargs, cls)
        query = get_where_query(cls, kwargs)
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


if __name__ == "__main__":
    pass
