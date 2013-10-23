'''
Implements CSS3 functional notation.
'''

from . import bifunc
from ..types import Color


@bifunc
def rgb(red, green, blue):
    return Color((red, green, blue), ctype='rgb')


@bifunc
def rgba(red, green, blue, alpha):
    return Color((red, green, blue, alpha), ctype='rgba')
