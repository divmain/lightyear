from textwrap import dedent

import env
from lightyear import LY


# COLOR OPERATIONS

def test_grid_a():
    i = dedent('''
        // Configure primary grid with 16 columns.
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
        //  - consumes 8 columns of parent grid.
        //  - configures 3 inner columns
        //  - configures gutter of 64px for inner columns
        ngrid-1-parent = 0
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


def test_grid_nested_b():
    i = dedent('''
        // Configure primary grid with 16 columns.
        grid-columns = 16
        grid-column-width = 60px
        grid-gutter = 32px

        // Configure nested grid
        //  - consumes 8 columns of parent grid.
        //  - configures 4 inner columns
        //  - configures gutter of 64px for inner columns
        ngrid-1-parent = 0
        ngrid-1-ocolumns = 8
        ngrid-1-icolumns = 4
        ngrid-1-gutter = 64px

        // Second-level nested grid
        //  - consumes 2 columns of parent nested grid (1).
        //  - configures 3 inner columns
        //  - configures gutter of 4px
        ngrid-2-parent = 1
        ngrid-2-ocolumns = 2
        ngrid-2-icolumns = 3
        ngrid-2-gutter = 4px

        .outside
            col(8)

        .inside
            ncol(1 1)

        .second
            ncol(2 1)
        ''')

    o = ('.outside{box-sizing:border-box;display:inline-block;width:480px;margin-left:16px;margin-right:16px;}'
         '.inside{box-sizing:border-box;display:inline-block;width:112px;margin-left:32px;margin-right:32px;}'
         '.second{box-sizing:border-box;display:inline-block;width:53.3333px;margin-left:2px;margin-right:2px;}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_grid_nested_c():
    i = dedent('''
        // Configure primary grid with 16 columns.
        grid-columns = 16
        grid-column-width = 60px
        grid-gutter = 32px

        // Configure nested grid
        //  - consumes 8 columns of parent grid.
        //  - configures 4 inner columns
        //  - configures gutter of 64px for inner columns
        ngrid-1-parent = 0
        ngrid-1-ocolumns = 8
        ngrid-1-icolumns = 4
        ngrid-1-gutter = 64px

        // Second-level nested grid
        //  - consumes 2 columns of parent nested grid (1).
        //  - configures 3 inner columns
        //  - configures gutter of 4px
        ngrid-2-parent = 1
        ngrid-2-ocolumns = 2
        ngrid-2-icolumns = 3
        ngrid-2-gutter = 4px

        // Second-level nested grid
        //  - consumes 3 columns of parent nested grid (1).
        //  - configures 2 inner columns
        //  - configures gutter of 8px
        ngrid-3-parent = 1
        ngrid-3-ocolumns = 3
        ngrid-3-icolumns = 2
        ngrid-3-gutter = 8px

        .outside
            col(8)

        .inside
            ncol(1 1)

        .secondA
            ncol(2 1)

        .secondB
            ncol(3 2)
        ''')

    o = ('.outside{box-sizing:border-box;display:inline-block;width:480px;margin-left:16px;margin-right:16px;}'
         '.inside{box-sizing:border-box;display:inline-block;width:112px;margin-left:32px;margin-right:32px;}'
         '.secondA{box-sizing:border-box;display:inline-block;width:53.3333px;margin-left:2px;margin-right:2px;}'
         '.secondB{box-sizing:border-box;display:inline-block;width:272px;margin-left:4px;margin-right:4px;}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o
