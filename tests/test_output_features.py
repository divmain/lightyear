from textwrap import dedent

import env
from lightyear import LY


### DEBUG ###

def test_debug_line_numbers():
    i = dedent('''
        div#one
            background-color: #44eeff
            display: block
            width: 32px
            height: 24px
        ''')
    o = ('div#one/*line2*/'
         '{background-color:#44eeff;/*line3*/'
         'display:block;/*line4*/'
         'width:32px;/*line5*/'
         'height:24px;/*line6*/}')
    ly = LY(debug=True)
    ly.eval(i)
    assert ly.css() == o


### PRETTY CSS ###

def test_pretty_css():
    i = dedent('''
        div.main
            color: blue
            width: 800px
            a
                text-decoration: none
        ''')
    o = ('div.main {\n'
         '    color: blue;\n'
         '    width: 800px;\n'
         '}\n'
         'div.main a {\n'
         '    text-decoration: none;\n'
         '}\n')
    ly = LY()
    ly.eval(i)
    assert ly.pretty_css() == o


def test_pretty_css_debug():
    i = dedent('''
        div.main
            color: blue
            width: 800px
            a
                text-decoration: none
        ''')
    o = ('div.main /*line2*/ {\n'
         '    color: blue; /*line3*/\n'
         '    width: 800px; /*line4*/\n'
         '}\n'
         'div.main a /*line5*/ {\n'
         '    text-decoration: none; /*line6*/\n'
         '}\n')
    ly = LY(debug=True)
    ly.eval(i)
    assert ly.pretty_css() == o
