# Let's make a Postgres storage system for sim data
from matplotlib import pyplot as plt
import numpy as np
from typing import Iterable
from store.util import get_where_query


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


if __name__ == "__main__":
    pass
