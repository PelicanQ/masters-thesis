# Let's make a Postgres storage system for sim data
from matplotlib import pyplot as plt
import numpy as np
from functools import reduce
from operator import or_
from typing import Iterable
import math

tol = 1e-6


def approx_in(field, values):
    conditions = [field.between(v - tol, v + tol) for v in values]
    return reduce(or_, conditions)


def meshline_query(cls, kwargs):
    # the idea is that one of kwargs is an iterable and we return entries with those values in ascending order
    iterable_key = get_iterable_key(kwargs)
    query = cls.model.select()
    iterable = kwargs[iterable_key]
    num = len(iterable)
    for key, val in kwargs.items():
        # the fixed ones
        if key != iterable_key:
            query = query.where(getattr(cls.model, key).between(val - tol, val + tol))
    chunk = 20
    ranges = [iterable[chunk * i : chunk * (i + 1)] for i in range(math.ceil(num / chunk))]
    # print(partial1, partial2)
    iterable_field = getattr(cls.model, iterable_key)
    query_parts = [query.where(approx_in(iterable_field, part_range)) for part_range in ranges]
    query = reduce(lambda a, b: a.union(b), query_parts)
    # print(kwargs)
    if len(query) != len(iterable):
        raise Exception("Requested variables could not be found")
    return query


def line_query(cls, kwargs):
    missing_key = get_missing_key(kwargs, cls)
    query = get_where_query(cls, kwargs)
    vars = []
    results = {key: [] for key in cls.all_vals}
    for entry in query:
        vars.append(getattr(entry, missing_key))
        for column in cls.all_vals:
            results[column].append(getattr(entry, column))
    if len(vars) < 1:
        raise Exception("It seems no line was not found for given values")
    return np.array(vars), *(np.array(results[val]) for val in cls.all_vals)


def get_missing_key(kwargs, cls):
    keys = kwargs.keys()
    missing_keys = list(filter(lambda s: s not in keys, cls.all_keys))
    if len(missing_keys) != 1:
        raise Exception("One key must be undefined")
    missing_key = missing_keys[0]
    print("variable: ", missing_key)

    return missing_key


def get_where_query(cls, kwargs):
    query = cls.model.select()
    for key, val in kwargs.items():
        query = query.where(getattr(cls.model, key).between(val - tol, val + tol))
    return query


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


def filter_points(candidates, lattice):
    """Given some candidate points, return boolan mask of which candidates are close to some lattice point"""
    v = np.tile(candidates, (len(lattice), 1))  # duplicate over one row per lattice point
    diff = (v.T - lattice).T
    boolmatrix = np.abs(diff) < tol
    mask = np.any(boolmatrix, axis=0)  # As long as one column has a True, that poinit should be included
    # mask is not a 1D array telling which index of queried entry to keep
    return mask


def parameter_index_map(values: Iterable, ndecimals: int):
    """For fast lookup on what index a float in a list has"""
    map = dict()
    for i, val in enumerate(values):
        map[round(float(val), ndecimals)] = i
    return map


def filter_grid(cls, kwargs, var1: str, val1: Iterable, ndigits1: int, var2: str, val2: Iterable, ndigits2: int):
    grid_size = len(val1) * len(val2)  # how many points in request grid?
    query = get_where_query(cls, kwargs)
    var1_candidates = np.ones((len(query),))
    var2_candidates = np.ones((len(query),))
    candidates = []
    # extract var1 and var2 from all rows
    for i, entry in enumerate(query):
        candidates.append(entry)
        var1_candidates[i] = getattr(entry, var1)
        var2_candidates[i] = getattr(entry, var2)
    # Imagine a 2D lattice formed by the cartesian product of val1 * val2
    # We form two 1D arrays. One such indicates whether a db point has its var1 value to some val1 value. Likewise for var2 val2
    var1_mask = filter_points(var1_candidates, val1)
    var2_mask = filter_points(var2_candidates, val2)
    keep = np.all(
        np.array([var1_mask, var2_mask]), axis=0
    )  # this indicates whether a db point intersect in both dimensions
    if np.count_nonzero(keep) != grid_size:
        raise Exception("Number of found points don't match grid size")
    print(np.count_nonzero(keep), grid_size)
    # for faster insert, form map between vars and index in query
    index_map1 = parameter_index_map(val1, ndigits1)
    index_map2 = parameter_index_map(val2, ndigits2)

    filtered = filter(lambda item: keep[item[0]], enumerate(candidates))  # filter for the ones to keep
    points = map(lambda item: item[1], filtered)  # extract the point
    return points, index_map1, index_map2


if __name__ == "__main__":
    l = [str(n) for n in range(10)]
    f = filter(lambda item: item[0] % 2 == 0, enumerate(l))
    r = map(lambda item: item[1], f)
    print(list(r))
