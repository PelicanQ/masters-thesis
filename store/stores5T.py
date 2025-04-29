import numpy as np
from store.models5T import ZZ5T_triang
from store.util import get_missing_key, get_where_query, meshline_query, filter_grid
from store.stores import StoreBase


class Store_zz5T_triang(StoreBase):
    all_keys = [
        "Ej1",
        "Ej2",
        "Ej3",
        "Ej4",
        "Ej5",
        "Eint12",
        "Eint13",
        "Eint23",
        "Eint34",
        "Eint35",
        "Eint45",
    ]

    all_vals = ["zz13", "zz35", "zz13", "zzz135"]
    model = ZZ5T_triang

    @classmethod
    def insert_many(cls, results: list[dict]):
        for res in results:
            fields = [(field, res[field]) for field in (cls.all_keys + cls.all_vals)]
            # this selection excludes k. We don't insert k
            cls.insert(**dict(fields))

    @staticmethod
    def insert(Ej1, Ej2, Ej3, Ej4, Ej5, Eint12, Eint23, Eint13, Eint34, Eint45, Eint35, zz13, zz35, zz15, zzz135):
        # accept k parameter but ignore
        return ZZ5T_triang.replace(
            Ej1=round(Ej1, 1),
            Ej2=round(Ej2, 1),
            Ej3=round(Ej3, 1),
            Ej4=round(Ej4, 1),
            Ej5=round(Ej5, 1),
            Eint12=round(Eint12, 3),
            Eint23=round(Eint23, 3),
            Eint13=round(Eint13, 3),
            Eint34=round(Eint34, 3),
            Eint45=round(Eint45, 3),
            Eint35=round(Eint35, 3),
            zz13=zz13,
            zz35=zz35,
            zz15=zz15,
            zzz135=zzz135,
        ).execute()

    @classmethod
    def get_all(cls):
        results = {key: [] for key in cls.all_vals}
        query = cls.model.select()
        for entry in query:
            for column in cls.all_vals:
                results[column].append(getattr(entry, column))

        return results["zz13"], results["zz35"], results["zz15"], results["zzz135"]

    @classmethod
    def line(cls, **kwargs):
        missing_key = get_missing_key(kwargs, cls)
        query = get_where_query(cls, kwargs)
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
        return results["zz13"], results["zz35"], results["zz15"], results["zzz"]

    @classmethod
    def plane(cls, var1: str, val1: np.ndarray, ndigits1: int, var2: str, val2: np.ndarray, ndigits2: int, **kwargs):
        """val1 and val2 must be 1D numpy vectors"""
        points, index_map1, index_map2 = filter_grid(cls, kwargs, var1, val1, ndigits1, var2, val2, ndigits2)
        print(index_map2)
        zz13 = np.zeros((len(val2), len(val1)))
        zz13[:] = np.nan
        zz35 = zz13.copy()
        zz15 = zz13.copy()
        zzz135 = zz13.copy()

        for point in points:
            varval1 = getattr(point, var1)
            varval2 = getattr(point, var2)
            index1 = index_map1[round(varval1, ndigits1)]
            index2 = index_map2[round(varval2, ndigits2)]
            zz13[index2, index1] = point.zz13
            zz35[index2, index1] = point.zz35
            zz15[index2, index1] = point.zz15
            zzz135[index2, index1] = point.zzz135

        return zz13, zz35, zz15, zzz135  # note: these are all with Gale Shapely
