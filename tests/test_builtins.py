from textwrap import dedent

import env
from lightyear import LY


# COLOR OPERATIONS

def test_darken_a():
    i = dedent('''
        p
            color: darken(#ffffff 10%)
        ''')
    o = 'p{color:#e5e5e5;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_darken_b():
    i = dedent('''
        p
            color: darken(#ffffff #111111)
        ''')
    o = 'p{color:#eeeeee;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_darken_c():
    i = dedent('''
        p
            color: darken(#ffffff 10)
        ''')
    o = 'p{color:#f5f5f5;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_darken_d():
    i = dedent('''
        p
            color: darken(#ff1537 50)
        ''')
    o = 'p{color:#cd0005;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_darken_e():
    i = dedent('''
        p
            color: darken(#ff1537 #8e114a)
        ''')
    o = 'p{color:#710400;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_lighten_a():
    i = dedent('''
        p
            color: lighten(#202020 10%)
        ''')
    o = 'p{color:#232323;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_lighten_b():
    i = dedent('''
        p
            color: lighten(#404040 #101010)
        ''')
    o = 'p{color:#505050;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_lighten_c():
    i = dedent('''
        p
            color: lighten(#000000 10)
        ''')
    o = 'p{color:#0a0a0a;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_lighten_d():
    i = dedent('''
        p
            color: lighten(#dc2c5c 50)
        ''')
    o = 'p{color:#ff5e8e;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_lighten_e():
    i = dedent('''
        p
            color: lighten(#96fa42 #69060c)
        ''')
    o = 'p{color:#ffff4e;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o
