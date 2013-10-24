from textwrap import dedent

import env
from lightyear import LY


# COLOR OPERATIONS

def test_grid_a():
    i = dedent('''
        // Configure primary grid with 16 columns.
        grid-columns = 16
        grid-column-width = 60px
        grid-gutter = 32px

        .thing
            col(8)
        ''')

    o = ('.thing{box-sizing:border-box;display:inline-block;width:480px;margin-left:16px;margin-right:16px;}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_grid_nested_a():
    i = dedent('''
        // Configure primary grid with 16 columns.
        grid-columns = 16
        grid-column-width = 60px
        grid-gutter = 32px

        // Configure nested grid
        //  - assumes space of 8 columns of parent grid.
        //  - configures 3 inner columns
        //  - configured gutter of 64px for inner columns
        ngrid-1-ocolumns = 8
        ngrid-1-icolumns = 4
        ngrid-1-gutter = 64px

        .outside
            col(8)

        .inside
            ncol(1 1)
        ''')

    o = ('.outside{box-sizing:border-box;display:inline-block;width:480px;margin-left:16px;margin-right:16px;}'
         '.inside{box-sizing:border-box;display:inline-block;width:112px;margin-left:32px;margin-right:32px;}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o
