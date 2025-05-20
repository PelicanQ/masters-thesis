# Let's make a Postgres storage system for sim data
from matplotlib import pyplot as plt
import numpy as np
from typing import Iterable
from store.util import get_where_query
import time


class StoreBase:
    @classmethod
    def check_exists(cls, **kwargs):
        """To avoid duplicate eig work, use this to see if data already exists"""
        # This only checks one row. For checking many, I should create a method to get all + filter in python
        keys = list(filter(lambda key: key in cls.all_keys, kwargs.keys()))
        if len(keys) != len(cls.all_keys):
            raise Exception("Please supply all keys")
        query = get_where_query(cls, dict([(key, kwargs[key]) for key in keys]))
        # in case some float rounding artifact has inserted what we consider duplicates
        return query.count() >= 1

    @classmethod
    def filter_existing(cls, jobs: list[dict]):
        """
        For a run, there may be many unchanging parameters and only a few changing.
        For performance, supply static and list of dynamic job kwargs.
        It is assumed that static + dynamic give the full composite key.
        Jobs which don't exist are returned
        """
        ref_job = jobs[0].copy()
        static_kwargs = {key: ref_job[key] for key in cls.all_keys}
        dynamic_kwargs: set[str] = set()

        # go through jobs and compare to reference job. discard those kwargs which change
        # t1 = time.perf_counter()
        for job in jobs[1:]:
            for key in job.keys():
                if abs(ref_job[key] - job[key]) > 1e-6:
                    # this kwargs is not static
                    static_kwargs.pop(key, False)
                    dynamic_kwargs.add(key)
        # t2 = time.perf_counter()
        # print("key", t2 - t1)

        # now we can make a smaller query compared to getting the whole table
        query = get_where_query(cls, static_kwargs)

        def matches(job, row):
            # return if they match on the dynamic kwargs
            for key in dynamic_kwargs:
                if abs(job[key] - getattr(row, key)) > 1e-6:
                    return False
            return True

        def has_match(job):
            for row in query:
                if matches(job, row):
                    return True
            return False

        filtered = []
        for job in jobs:
            if not has_match(job):
                filtered.append(job)
        # t3 = time.perf_counter()
        # print("filter", t3 - t2)
        return filtered


if __name__ == "__main__":
    pass
