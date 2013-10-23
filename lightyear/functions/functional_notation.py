'''
Implements CSS3 functional notation.
'''

from . import bifunc
from ..types import Color


### SYNTAX

@bifunc
def url(text):
    return 'url({})'.format(text)


### COLORS

@bifunc
def rgb(red, green, blue):
    return Color((red, green, blue), ctype='rgb')


@bifunc
def rgba(red, green, blue, alpha):
    return Color((red, green, blue, alpha), ctype='rgba')


@bifunc
def hsl(hue, saturation, lightness):
    return Color((hue, saturation, lightness), ctype='hsl')


@bifunc
def hsla(hue, saturation, lightness, alpha):
    return Color((hue, saturation, lightness, alpha), ctype='hsla')
