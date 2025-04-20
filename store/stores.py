# Let's make a Postgres storage system for sim data
from matplotlib import pyplot as plt
import numpy as np
from store.models import Levels2T, ZZ2T, ZZ3T, Levels3T
from functools import reduce
from operator import or_
from typing import Iterable
import math
from store.util import filter_grid, meshline_query, get_missing_key, get_where_query, line_query


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
        missing_key = get_missing_key(kwargs, cls)
        query = get_where_query(kwargs, cls)
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
            Ec2=round(Ec2, 2), Ej1=round(Ej1, 1), Ej2=round(Ej2, 1), Eint=round(Eint, 2), **level_dict
        ).execute()

    @classmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            cls.insert(res["Ec2"], res["Ej1"], res["Ej2"], res["Eint"], res["levels"])

    @classmethod
    def line(cls, **kwargs):
        missing_key = get_missing_key(kwargs, cls)
        query = get_where_query(kwargs, cls)
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
        return line_query(cls, kwargs)

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
    def plane_fast(
        cls, var1: str, val1: np.ndarray, ndigits1: int, var2: str, val2: np.ndarray, ndigits2: int, **kwargs
    ):
        """val1 and val2 must be 1D numpy vectors"""
        points, index_map1, index_map2 = filter_grid(cls, kwargs, var1, val2, ndigits1, var2, val2, ndigits2)

        zz12 = np.zeros((len(val2), len(val1)))
        zz12[:] = np.nan
        zz23 = zz12.copy()
        zz13 = zz12.copy()
        zzz = zz12.copy()

        for point in points:
            varval1 = getattr(point, var1)
            varval2 = getattr(point, var2)
            index1 = index_map1[round(varval1, ndigits1)]
            index2 = index_map2[round(varval2, ndigits2)]
            zz12[index2, index1] = point.zzGS12
            zz23[index2, index1] = point.zzGS23
            zz13[index2, index1] = point.zzGS13
            zzz[index2, index1] = point.zzzGS

        return zz12, zz23, zz13, zzz  # note: these are all with Gale Shapely


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
        query = get_where_query(kwargs, cls)
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
