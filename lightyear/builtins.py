from decimal import Decimal
from .types import Color, Distance


def darken(color, amount):
    if not isinstance(color, Color):
        raise ValueError('Cannot darken non-color:', str(color))

    if isinstance(amount, Decimal):
        new_r = int(color._r - amount)
        new_g = int(color._g - amount)
        new_b = int(color._b - amount)
        color._r, color._g, color._b = (color if color >= 0 else 0
                                        for color in (new_r, new_g, new_b))
        return color

    elif isinstance(amount, Color):
        new_r = int(color._r - amount._r)
        new_g = int(color._g - amount._g)
        new_b = int(color._b - amount._b)
        color._r, color._g, color._b = (color if color >= 0 else 0
                                        for color in (new_r, new_g, new_b))
        return color

    elif isinstance(amount, Distance) and amount.unit == '%':
        new_r = int(color._r * (100 - amount.value) / 100)
        new_g = int(color._r * (100 - amount.value) / 100)
        new_b = int(color._r * (100 - amount.value) / 100)
        color._r, color._g, color._b = (color if color >= 0 else 0
                                        for color in (new_r, new_g, new_b))
        return color

    raise ValueError('Cannot darken by value:', str(amount))


def lighten(color, amount):
    if not isinstance(color, Color):
        raise ValueError('Cannot lighten non-color:', str(color))

    if isinstance(amount, Decimal):
        new_r = int(color._r + amount)
        new_g = int(color._g + amount)
        new_b = int(color._b + amount)
        color._r, color._g, color._b = (color if color <= 255 else 255
                                        for color in (new_r, new_g, new_b))
        return color

    elif isinstance(amount, Color):
        new_r = int(color._r + amount._r)
        new_g = int(color._g + amount._g)
        new_b = int(color._b + amount._b)
        color._r, color._g, color._b = (color if color <= 255 else 255
                                        for color in (new_r, new_g, new_b))
        return color

    elif isinstance(amount, Distance) and amount.unit == '%':
        new_r = int(color._r * (100 + amount.value) / 100)
        new_g = int(color._r * (100 + amount.value) / 100)
        new_b = int(color._r * (100 + amount.value) / 100)
        color._r, color._g, color._b = (color if color <= 255 else 255
                                        for color in (new_r, new_g, new_b))
        return color

    raise ValueError('Cannot lighten by value:', str(amount))


builtin_funcs = {
    'darken': darken,
    'lighten': lighten,
    }
