from textwrap import dedent

import env
from lightyear import LY


def test_rgb_a():
    i = dedent('''
        p
            color: rgb(22 56 12)
        ''')
    o = 'p{color:rgb(22,56,12);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_rgb_darken_a():
    i = dedent('''
        p
            color: darken(rgb(255 255 255) 10%)
        ''')
    o = 'p{color:rgb(229.5,229.5,229.5);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_hsl_darken_a():
    i = dedent(r'''
        p
            color: hsl(190 30% 94%)
        ''')
    o = 'p{color:hsl(190,30%,94%);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_hsl_darken_b():
    i = dedent(r'''
        p
            color: darken(hsl(190 30% 94%) 10%)
        ''')
    o = 'p{color:hsl(190,30%,84.6%);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


# def test_darken_b():
#     i = dedent('''
#         p
#             color: darken(#ffffff #111111)
#         ''')
#     o = 'p{color:#eeeeee;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o


# def test_darken_c():
#     i = dedent('''
#         p
#             color: darken(#ffffff 10)
#         ''')
#     o = 'p{color:#f5f5f5;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o


# def test_darken_d():
#     i = dedent('''
#         p
#             color: darken(#ff1537 50)
#         ''')
#     o = 'p{color:#cd0005;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o


# def test_darken_e():
#     i = dedent('''
#         p
#             color: darken(#ff1537 #8e114a)
#         ''')
#     o = 'p{color:#710400;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o


# def test_darken_f():
#     i = dedent('''
#         p
#             color: darken(white 10%)
#         ''')
#     o = 'p{color:#e5e5e5;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o


# def test_darken_g():
#     i = dedent('''
#         p
#             color: darken(white #ff9bff)
#         ''')
#     o = 'p{color:darkgreen;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o

