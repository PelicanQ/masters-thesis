import itertools
def get_iterable_keys(kwargs):
    # intended for when one key is iterable
    iterable_names = []
    for key, val in kwargs.items():
        try:
            iter(val)
            iterable_names.append(key)
        except:
            pass
    if len(iterable_names) == 0:
        raise Exception("You need some iterable")
    return iterable_names


def collect_jobs(**kwargs):
    # find iterables among given kwargs, loop over them and run zz
    iterables = get_iterable_keys(kwargs)
    arguments = kwargs.copy()
    jobs: list[dict] = []
    for tup in itertools.product(*[kwargs[itkey] for itkey in iterables]):
        # tuple now contains one point in the grid
        items = [(iterables[i], tup[i]) for i in range(len(iterables))]  # list of (key, value) pairs
        arguments.update(items)  # update the changing parameters
        jobs.append(arguments.copy())
    return jobs