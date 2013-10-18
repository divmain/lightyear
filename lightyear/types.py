from decimal import Decimal

from .errors import IncompatibleUnits

class RuleBlock():
    def __init__(self, tag, selectors, block):
        self.tag = tag
        self.selectors = selectors
        self.block = block


class CSSRule():
    def __init__(self, tag, prop, values):
        self.tag = tag
        self.prop = prop
        self.values = values


class MixIn():
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, *args):
        return self.func(*args)


class RootBlock():
    def __init__(self, tag_name, prefix):
        self.tag_name = tag_name
        self.prefix = prefix


class Distance():
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __add__(self, other):
        if isinstance(other, Decimal):
            return Distance(self.value + other, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(self.value + other.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be added to unit {}.'.format(
                self.unit, other.unit))

    def __sub__(self, other):
        if isinstance(other, Decimal):
            return Distance(self.value - other, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(self.value - other.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be subtracted from unit {}.'.format(
                self.unit, other.unit))

    def __mul__(self, other):
        if isinstance(other, Decimal):
            return Distance(self.value * other, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(self.value * other.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be multiplied with unit {}.'.format(
                self.unit, other.unit))

    def __div__(self, other):
        if isinstance(other, Decimal):
            return Distance(self.value / other, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(self.value / other.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be divided by unit {}.'.format(
                self.unit, other.unit))

    def __eq__(self, other):
        if isinstance(other, Distance) and other.unit == self.unit:
            return self.value == other.value
        raise IncompatibleUnits(
            'Unit {} cannot be divided by unit {}.'.format(
                self.unit, other.unit))
