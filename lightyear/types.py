from decimal import Decimal

from lightyear.errors import IncompatibleUnits


class RuleBlock():
    def __init__(self, tag, selectors, block):
        self.tag = tag
        self.selectors = selectors
        self.block = block

    def css(self):
        if not len(self.block):
            return ''
        outside = ','.join(self.selectors)
        inside = ' '.join(e.css() if hasattr(e, 'css') else '{} {}'.format(type(e), repr(e))  # ''
                          for e in self.block)
        return outside + " {" + inside + "}"

    def parent_selectors(self):
        for i, element in reversed(list(enumerate(self.block))):
            if isinstance(element, ParentSelector):
                yield element
                del self.block[i]


class CSSRule():
    def __init__(self, tag, prop, values):
        self.tag = tag
        self.prop = prop
        self.values = values

    def css(self):
        print('prop', self.prop)
        print('values', self.values)
        return self.prop + ": " + " ".join(str(x) for x in self.values) + ";"


class ParentSelector():
    def __init__(self, rule_block):
        self.rule_block = rule_block


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

    def __str__(self):
        return str(self.value) + self.unit

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

    def __truediv__(self, other):
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
