from decimal import Decimal
from colorsys import hls_to_rgb, rgb_to_hls
from math import ceil

from .errors import IncompatibleUnits
from .globals import NAMED_COLORS


class RuleBlock():
    '''
    Represents a series of CSS selectors and any children objects, including
    nested RuleBlocks and CSS property/value declarations.
    '''
    def __init__(self, tag, selectors, block):
        self.tag = tag
        self.selectors = selectors
        self.block = block

    def css(self, tag=None):
        '''
        Return valid CSS for self and nested property/value declarations.
        '''
        if not len(self.block):
            return ''
        if self.tag and not tag == self.tag:
            return ''
        outside = ' '.join(self.selectors)

        if self.tag:
            inside = ''.join(
                e.css() if hasattr(e, 'css')
                else '{} {}'.format(type(e), repr(e))
                for e in self.block)
        else:
            inside = ''.join(
                e.css(tag=tag) if hasattr(e, 'css')
                else '{} {}'.format(type(e), repr(e))
                for e in self.block)

        if not inside:
            return ''
        return outside + "{" + inside + "}"


class AtRuleBlock():
    '''
    Represents a CSS at-rule and any children objects.
    '''
    def __init__(self, tag, text, block):
        self.tag = tag
        self.text = text
        self.block = block

    def css(self, tag=None):
        '''
        Return valid CSS for self and nested property/value declarations.
        '''
        if not len(self.block):
            return ''
        if self.tag and not tag == self.tag:
            return ''
        outside = '@' + self.text

        if self.tag:
            inside = ''.join(
                e.css() if hasattr(e, 'css')
                else '{} {}'.format(type(e), repr(e))
                for e in self.block)
        else:
            inside = ''.join(
                e.css(tag=tag) if hasattr(e, 'css')
                else '{} {}'.format(type(e), repr(e))
                for e in self.block)

        if not inside:
            return ''

        return outside + "{" + inside + "}"


class Keyframe():
    '''
    Represents a keyframe in a CSS animation.
    '''
    def __init__(self, tag, condition, block):
        self.tag = tag
        self.condition = condition
        self.block = block

    def css(self, tag=None):
        '''
        Return CSS representation.
        '''
        if not len(self.block):
            return ''
        if self.tag and not tag == self.tag:
            return ''
        outside = self.condition

        if self.tag:
            inside = ''.join(
                e.css() if hasattr(e, 'css')
                else '{} {}'.format(type(e), repr(e))
                for e in self.block)
        else:
            inside = ''.join(
                e.css(tag=tag) if hasattr(e, 'css')
                else '{} {}'.format(type(e), repr(e))
                for e in self.block)

        if not inside:
            return ''

        return str(outside) + "{" + inside + "}"


class CSSRule():
    '''
    Represents CSS property/value declarations.
    '''
    def __init__(self, tag, prop, values):
        self.tag = tag
        self.prop = prop
        self.values = values

    def css(self, tag=None):
        '''
        Return valid CSS for self.
        '''
        if tag and not tag == self.tag:
            return ''
        if self.tag and not tag:
            return ''
        return self.prop + ":" + " ".join(str(x) for x in self.values) + ";"


class ParentSelector():
    '''
    LightYear rule blocks that start with a reference to their parent.
    Example:
    p
        &:hover   <---   ParentSelector will be used here.
    '''
    def __init__(self, rule_block):
        self.rule_block = rule_block


class MixIn():
    '''
    Represents mixins and basic functions defined within LightYear code.
    '''
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, *args):
        return self.func(*args)


class UnpackMe(list):
    '''
    Contains results of mixin calls that need to be incorporated into their
    parent RuleBlocks.
    '''
    def css(self, tag=None):
        return ''


class RootBlock():
    '''
    Represents root blocks that specify what CSS to output.
    '''
    def __init__(self, tag_name, prefix):
        self.tag_name = tag_name
        self.prefix = prefix


class IgnoreMe():
    '''
    To replace RuleBlocks or other objects that should not be evaluated when
    producing CSS.
    '''
    def css(self, tag=None):
        return ''


class Distance():
    '''
    Represents CSS numerical values used for measurement.
    '''
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

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Decimal):
            return Distance(self.value - other, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(self.value - other.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be subtracted from unit {}.'.format(
                self.unit, other.unit))

    def __rsub__(self, other):
        if isinstance(other, Decimal):
            return Distance(other - self.value, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(other.value - self.value, self.unit)
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

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Decimal):
            return Distance(self.value / other, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(self.value / other.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be divided by unit {}.'.format(
                self.unit, other.unit))

    def __rtruediv__(self, other):
        if isinstance(other, Decimal):
            return Distance(other / self.value, self.unit)
        elif isinstance(other, Distance) and other.unit == self.unit:
            return Distance(other.value / self.value, self.unit)
        raise IncompatibleUnits(
            'Unit {} cannot be divided by unit {}.'.format(
                self.unit, other.unit))

    def __eq__(self, other):
        if isinstance(other, Distance) and other.unit == self.unit:
            return self.value == other.value
        raise IncompatibleUnits(
            'Unit {} cannot be divided by unit {}.'.format(
                self.unit, other.unit))


class Color():
    '''
    Represents a CSS color.
    '''
    def __init__(self, color, ctype):
        self.type = ctype

        if ctype == 'named':
            self.name = color

        elif ctype == 'hex':
            if not len(color) == 7:
                raise ValueError('Invalid hexidecimal color.')
            self.hex = color

        elif ctype == 'rgb':
            self.rgb = color

        elif ctype == 'rgba':
            self.rgba = color

        elif ctype == 'hsl':
            self.hsl = color

        elif ctype == 'hsla':
            self.hsla = color

    @property
    def rgba(self):
        return 'rgba({r},{g},{b},{a}'.format(
            r=self._r,
            g=self._g,
            b=self._b,
            a=self._a)

    @rgba.setter
    def rgba(self, color):
        self._r, self._g, self._b, self._a = color

    @property
    def rgb(self):
        return 'rgb({r},{g},{b})'.format(
            r=self._r,
            b=self._b,
            g=self._g)

    @rgb.setter
    def rgb(self, color):
        self.rgba = tuple(color) + (Decimal('1'), )

    @property
    def hex(self):
        return '#{r:0>2x}{g:0>2x}{b:0>2x}'.format(
            r=int(self._r),
            g=int(self._g),
            b=int(self._b))

    @hex.setter
    def hex(self, text):
        self.rgb = (
            int(color, 16)
            for color in (text[1:3], text[3:5], text[5:7])
            )

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, text):
        self._name = text
        self.hex = NAMED_COLORS[text]

    @property
    def hsla(self):
        rnd = lambda x: ceil(x * 10000) / Decimal('10000')

        r, g, b = float(self._r / 255), float(self._g / 255), float(self._b / 255)
        h, l, s = rgb_to_hls(r, g, b)

        h = rnd(360 * h)
        s = rnd(100 * s)
        l = rnd(100 * l)

        return 'hsla({h},{s}%,{l}%,{a})'.format(
            h=h,
            s=s,
            l=l,
            a=self._a)

    @hsla.setter
    def hsla(self, color):
        rnd = lambda x: ceil(x * 10000) / Decimal('10000')

        h, s, l, a = color
        if not (isinstance(h, Decimal) and
                isinstance(s, Distance) and s.unit == '%' and
                isinstance(l, Distance) and s.unit == '%' and
                isinstance(a, Decimal)):
            raise ValueError('Function hsl/hsla requires whole number for h and percent for s and l.')

        h /= 360
        s = s.value / 100
        l = l.value / 100

        self._r, self._g, self._b = (255*rnd(x) for x in hls_to_rgb(float(h), float(l), float(s)))

        self._a = a

    @property
    def hsl(self):
        return ','.join(self.hsla.split(',')[:-1]).replace('hsla', 'hsl') + ')'

    @hsl.setter
    def hsl(self, color):
        self.hsla = tuple(color) + (Decimal('1'), )

    def __str__(self):
        if self.type == 'rgb':
            return self.rgb
        elif self.type == 'rgba':
            return self.rgba
        elif self.type == 'hex':
            return self.hex
        elif self.type == 'hsl':
            return self.hsl
        elif self.type == 'hsla':
            return self.hsla

        # self.type == 'named'
        if (self._name in NAMED_COLORS and NAMED_COLORS[self._name] == self.hex):
            return self._name

        _hex = self.hex
        for name in NAMED_COLORS:
            if _hex == NAMED_COLORS[name]:
                return name

        return _hex
