import collections


class Lookup(object):
    def __init__(self, original_function):
        self.original, self.table = original_function, {}

    def __call__(self, *arguments):
        key = tuple([arg if isinstance(arg, collections.Hashable) else id(arg) for arg in arguments])
        if key in self.table:
            return self.table[key]
        result = self.original(*arguments)
        self.table[key] = result
        return result
