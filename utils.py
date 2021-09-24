import operator
from functools import reduce


def lookup(data, keys):
    return reduce(operator.getitem, keys, data)
