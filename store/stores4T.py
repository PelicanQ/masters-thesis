from matplotlib import pyplot as plt
import numpy as np
from store.models4T import ZZ4T
from functools import reduce
from operator import or_
from typing import Iterable
import math
from store.util import line_query, get_missing_key, get_where_query, filter_grid, meshline_query


class Store_zz4T:
    all_keys = ["Ej1", "Ej2", "Ej3", "Ej4" "Eint12", "Eint23", "Eint13", "Eint34"]
    all_vals = [
        "zz12",
        "zz23",
        "zz34",
        "zz13",
        "zz24",
        "zz14",
        "zzz123",
        "zzz234",
        "zzz124",
        "zzz134",
        "zzzz",
    ]
    model = ZZ4T

    @classmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            fields = [(field, res[field]) for field in (cls.all_keys + cls.all_vals)]
            # this selection excludes k. We don't insert k
            cls.insert(**dict(fields))

    @staticmethod
    def insert(
        Ej1,
        Ej2,
        Ej3,
        Ej4,
        Eint12,
        Eint23,
        Eint13,
        Eint34,
        zz12,
        zz23,
        zz34,
        zz13,
        zz24,
        zz14,
        zzz123,
        zzz234,
        zzz124,
        zzz134,
        zzzz,
    ):
        # accept k parameter but ignore
        return ZZ4T.replace(
            Ej1=round(Ej1, 1),
            Ej2=round(Ej2, 1),
            Ej3=round(Ej3, 1),
            Ej4=round(Ej4, 1),
            Eint12=round(Eint12, 3),
            Eint23=round(Eint23, 3),
            Eint13=round(Eint13, 3),
            Eint34=round(Eint34, 3),
            zz12=zz12,
            zz23=zz23,
            zz34=zz34,
            zz13=zz13,
            zz24=zz24,
            zz14=zz14,
            zzz123=zzz123,
            zzz234=zzz234,
            zzz124=zzz124,
            zzz134=zzz134,
            zzzz=zzzz,
        ).execute()

    @classmethod
    def get_all(cls):
        results = {key: [] for key in cls.all_vals}
        query = cls.model.select()
        for entry in query:
            for column in cls.all_vals:
                results[column].append(getattr(entry, column))

        return results

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
        return results

    @classmethod
    def plane_fast(
        cls, var1: str, val1: np.ndarray, ndigits1: int, var2: str, val2: np.ndarray, ndigits2: int, **kwargs
    ):
        """val1 and val2 must be 1D numpy vectors. Val2 == row dimension"""
        points, index_map1, index_map2 = filter_grid(cls, kwargs, var1, val1, ndigits1, var2, val2, ndigits2)
        val_mat = np.zeros((len(val2), len(val1)))
        val_mat[:] = np.nan
        results = {key: val_mat.copy() for key in cls.all_vals}

        for point in points:
            varval1 = getattr(point, var1)
            varval2 = getattr(point, var2)
            index1 = index_map1[round(varval1, ndigits1)]
            index2 = index_map2[round(varval2, ndigits2)]
            for column in cls.all_vals:
                results[column][index2, index1] = getattr(point, column)

        return results


if __name__ == "__main__":
    pass
