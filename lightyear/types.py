from collections import OrderedDict


class Scope(OrderedDict):
    def __getitem__(self, k):
        if not self.__contains__(k):
            self[k] = Scope()
        return super().__getitem__(k)


class Attribute(str):
    pass
