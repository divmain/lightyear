from decimal import Decimal

from . import bifunc
from ..types import UnpackMe, CSSRule
from ..errors import LyError


@bifunc
def col(env, number):
    try:
        column_width = env['grid-column-width']
        gutter = env['grid-gutter']
    except KeyError:
        raise LyError('Grid is not configured.')

    width = column_width * number
    margin = gutter / Decimal(2)

    declarations = [
        CSSRule(
            tag=None,
            prop='box-sizing',
            values=['border-box'],
            index='generated'),
        CSSRule(
            tag=None,
            prop='display',
            values=['inline-block'],
            index='generated'),
        CSSRule(
            tag=None,
            prop='width',
            values=[width],
            index='generated'),
        CSSRule(
            tag=None,
            prop='margin-left',
            values=[margin],
            index='generated'),
        CSSRule(
            tag=None,
            prop='margin-right',
            values=[margin],
            index='generated'),
        ]

    return UnpackMe(declarations)


@bifunc
def ncol(env, level, number):
    pass
