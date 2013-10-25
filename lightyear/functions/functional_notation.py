'''
Implements CSS3 functional notation.
'''

from . import bifunc
from ..types import Color


### SYNTAX ###

@bifunc
def url(env, text):
    return 'url({})'.format(text)


@bifunc
def toggle(env, text):
    return 'toggle({})'.format(text)


### VALUES AND UNITS ###

@bifunc
def calc(env, *args):
    return 'calc({})'.format(''.join(str(arg) for arg in args))


@bifunc
def attr(env, text):
    return 'attr({})'.format(text)


### COLORS ###

@bifunc
def rgb(env, red, green, blue):
    return Color((red, green, blue), ctype='rgb')


@bifunc
def rgba(env, red, green, blue, alpha):
    return Color((red, green, blue, alpha), ctype='rgba')


@bifunc
def hsl(env, hue, saturation, lightness):
    return Color((hue, saturation, lightness), ctype='hsl')


@bifunc
def hsla(env, hue, saturation, lightness, alpha):
    return Color((hue, saturation, lightness, alpha), ctype='hsla')


### CSS3 ###

@bifunc
def scale(env, x, y):
    return 'scale({x},{y})'.format(x=x, y=y)


### FONT-FACE ###

@bifunc
def format(env, text):
    return 'format("{}")'.format(text)
