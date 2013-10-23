from textwrap import dedent

import env
from lightyear import LY


### SYNTAX ###

def test_url():
    i = dedent('''
        div#header
            background-image: url("images/header.jpg")
        ''')
    o = 'div#header{background-image:url(images/header.jpg);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_toggle():
    i = dedent('''
        div#article
            font-style: toggle("italic, normal")
        ''')
    o = 'div#article{font-style:toggle(italic, normal);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


### VALUES AND UNITS ###

def test_calc():
    i = dedent('''
        section
            float: left
            margin: 1em
            border: solid 1px
            width: calc("100%/3 - 2*1em - " 2 * 1px)
        ''')
    o = 'section{float:left;margin:1em;border:solid 1px;width:calc(100%/3 - 2*1em - 2px);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_attr():
    i = dedent('''
        article
            width: attr("size em 0")
        ''')
    o = 'article{width:attr(size em 0);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


### COLORS ###

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


def test_hsl():
    i = dedent(r'''
        p
            color: hsl(190 30% 94%)
        ''')
    o = 'p{color:hsl(190,30%,94%);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_hsl_darken():
    i = dedent(r'''
        p
            color: darken(hsl(190 30% 94%) 10%)
        ''')
    o = 'p{color:hsl(190,30%,84.6%);}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o
