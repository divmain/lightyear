from decimal import Decimal

from . import bifunc
from ..types import UnpackMe, CSSRule
from ..errors import LyError


@bifunc
def col(env, number):
    '''
    Return declarations for a CSS column of size number.
    '''
    try:
        column_width = env['grid-column-width']
        gutter = env['grid-gutter']
    except KeyError as e:
        raise LyError('Grid is not properly configured. Cannot find: {}'.format(e))

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
def ncol(env, grid_id, number):
    '''
    Return CSS declarations for a nested column in grid_id of size number.
    '''
    try:
        total_columns = env['ngrid-{}-icolumns'.format(grid_id)]
        gutter = env['ngrid-{}-gutter'.format(grid_id)]
    except KeyError as e:
        raise LyError('Grid is not properly configured. Cannot find: {}'.format(e))

    width = grid_width(env, grid_id) / total_columns * number
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


def grid_width(env, grid_id):
    '''
    Return total grid width for grid with id grid_id.
    '''
    try:
        parent_id = env['ngrid-{}-parent'.format(grid_id)]
        if parent_id == 0:
            num_parent_consumed = env['ngrid-{}-ocolumns'.format(grid_id)]
            parent_column_width = env['grid-column-width']
            parent_gutter = env['grid-gutter']
            return parent_column_width * num_parent_consumed - parent_gutter

        parent_width = grid_width(env, parent_id)
        parent_gutter = env['ngrid-{}-gutter'.format(parent_id)]
        num_parent_columns = env['ngrid-{}-icolumns'.format(parent_id)]
        num_parent_consumed = env['ngrid-{}-ocolumns'.format(grid_id)]
        return (parent_width / num_parent_columns) * num_parent_consumed - parent_gutter

    except KeyError as e:
        raise LyError('Grid is not properly configured. Cannot find: {}'.format(e))
