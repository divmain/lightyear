import os.path
from textwrap import dedent

import env
from lightyear import LY


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_large_a():
    i = dedent('''
        body
            position: relative
            top: 80px

            > section
                padding: 40px 16px
                line-height: 1.4em

                .main
                    display: inline-block
                    width: 400px

                    .item
                        display: inline-block
                        width: 100px
                        margin-bottom: 24px

                    aside
                        display: inline-block
                        width: 100%

                h2
                    display: inline-block
                    width: 100px
        ''')
    o = ('body{position:relative;top:80px;}'
         'body > section{padding:40px 16px;line-height:1.4em;}'
         'body > section .main{display:inline-block;width:400px;}'
         'body > section .main .item{display:inline-block;width:100px;margin-bottom:24px;}'
         'body > section .main aside{display:inline-block;width:100%;}'
         'body > section h2{display:inline-block;width:100px;}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_example_file():
    with open(os.path.join(TEST_DIR, 'divmain.ly'), 'r') as f:
        i = f.read()
    with open(os.path.join(TEST_DIR, 'divmain.css'), 'r') as f:
        o = f.read()
    ly = LY()
    ly.eval(i)
    assert ly.pretty_css() == o


def test_example_vendorize():
    with open(os.path.join(TEST_DIR, 'divmain.ly'), 'r') as f:
        i = f.read()
    with open(os.path.join(TEST_DIR, 'divmain.vendor.css'), 'r') as f:
        o = f.read()
    ly = LY(vendorize='offline')
    ly.eval(i)
    assert ly.pretty_css() == o
