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
