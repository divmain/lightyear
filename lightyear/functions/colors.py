from decimal import Decimal
from colorsys import hls_to_rgb, rgb_to_hls

from . import bifunc
from ..types import Color, Distance


@bifunc
def darken(env, color, amount):
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
        r, g, b = float(color._r/255), float(color._g/255), float(color._b/255)
        h, l, s = rgb_to_hls(r, g, b)
        new_l = l * (100 - int(amount.value)) / 100
        color._r, color._g, color._b = (
            Decimal(255*c) if c >= 0 else Decimal(0)
            for c in hls_to_rgb(h, new_l, s))
        return color

    raise ValueError('Cannot darken by value:', str(amount))


@bifunc
def lighten(env, color, amount):
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
        r, g, b = float(color._r/255), float(color._g/255), float(color._b/255)
        h, l, s = rgb_to_hls(r, g, b)
        new_l = l * (100 + int(amount.value)) / 100
        color._r, color._g, color._b = (
            Decimal(255*c) if c <= 255 else Decimal(255)
            for c in hls_to_rgb(h, new_l, s))
        return color

    raise ValueError('Cannot lighten by value:', str(amount))
