from pprint import pformat
from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])


class Node:
    def __init__(self, index, path, value, room):
        self.index = index
        self.path = path
        self.value = value
        self.room = room

    def __repr__(self):
        return pformat(vars(self))

    def estimate(self, items):
        return self.value + sum(item.value for item in items[self.index:])

