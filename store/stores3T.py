import numpy as np
from store.models3T import ZZ3T
from store.util import filter_grid, meshline_query, line_query, get_iterable_key, get_missing_key, get_where_query
from store.stores import StoreBase
from store.models3T import Levels3T


class StoreLevels3T:
    all_keys = ["Ec2", "Ec3", "Ej1", "Ej2", "Ej3", "Eint12", "Eint23", "Eint13"]
    model = Levels3T
    max_level = 10

    @staticmethod
    def insert(Ec2, Ec3, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, levels):
        level_dict = dict([(f"E{i}", levels[i]) for i in range(len(levels))])
        return Levels3T.replace(
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


class Store_zz3T(StoreBase):
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
            Eint12=round(Eint12, 4),
            Eint23=round(Eint23, 4),
            Eint13=round(Eint13, 4),
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
    def plane(cls, var1: str, val1: np.ndarray, ndigits1: int, var2: str, val2: np.ndarray, ndigits2: int, **kwargs):
        """val1 and val2 must be 1D numpy vectors"""
        points, index_map1, index_map2 = filter_grid(cls, kwargs, var1, val1, ndigits1, var2, val2, ndigits2)

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
