from textwrap import dedent

import env
from lightyear import LY


def test_comments_a():
    i = dedent('''
        ////// this is a comment //////
        p
            color: #ffffff
        ''')
    o = 'p{color:#ffffff;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o
