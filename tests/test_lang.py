from textwrap import dedent

import env
from lightyear import LY


# SELECTORS

def test_simplest():
    i = 'body\n    width: 32px'
    o = 'body{width:32px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_type_sel():
    i = dedent('''
        body
            color: #000000
        ''')
    o = 'body{color:#000000;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_type_multiple_properties():
    i = dedent('''
        div
            color: #000000
            display: block
            width: 32px
        ''')
    o = 'div{color:#000000;display:block;width:32px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_multiple_values():
    i = dedent('''
        div
            color: #000000
            border: 1px 2px 3px 4px
        ''')
    o = 'div{color:#000000;border:1px 2px 3px 4px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_universal_sel():
    i = dedent('''
        *
            border: none
        ''')
    o = '*{border:none;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_attribute_sel():
    i = dedent('''
        a[class=happy]
            display: inline
        ''')
    o = 'a[class=happy]{display:inline;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_id_sel():
    i = dedent('''
        #first
            display: block
        ''')
    o = '#first{display:block;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_id_type_sel():
    i = dedent('''
        a#first
            display: block
        ''')
    o = 'a#first{display:block;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_pseudo_class_param():
    i = dedent('''
        li:nth-child(2)
            color: black
        ''')
    o = 'li:nth-child(2){color:black;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_pseudo_class_noparam():
    i = dedent('''
        a:hover
            color: white
        ''')
    o = 'a:hover{color:white;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


# def test_pseudo_class_not():
#     i = dedent('''
#         p:not(#example)
#             background-color: yellow
#         ''')
#     o = 'p:not(#example) {background-color: yellow;}'
#     ly = LY()
#     ly.eval(i)
#     assert ly.css() == o


def test_parent_selector_a():
    i = dedent('''
        p
            &#first
                background-color: yellow
        ''')
    o = 'p#first{background-color:yellow;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_parent_selector_b():
    i = dedent('''
        p
            a
                &#first
                    background-color: yellow
        ''')
    o = 'p a#first{background-color:yellow;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_parent_selector_c():
    i = dedent('''
        p
            a
                &:hover
                    background-color: yellow
        ''')
    o = 'p a:hover{background-color:yellow;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_multiple_scopes():
    i = dedent('''
        p
            color: #FFFFFF
        h2
            color: #DDDDDD
        ''')
    o = 'p{color:#ffffff;}h2{color:#dddddd;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


# NUMERIC

def test_addition():
    i = dedent('''
        li
            width: 8px + 2
        ''')
    o = 'li{width:10px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_subtraction():
    i = dedent('''
        .button
            left: 0px - 4px
        ''')
    o = '.button{left:-4px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_multiplication():
    i = dedent('''
        .button
            width: 4em * 8
        ''')
    o = '.button{width:32em;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_division_int():
    i = dedent('''
        div#first.button
            width: 20px / 4
        ''')
    o = 'div#first.button{width:5px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_division_float_a():
    i = dedent('''
        #last
            height: 10px / 4
        ''')
    o = '#last{height:2.5px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_division_float_b():
    i = dedent('''
        #last
            height: 10px / 3
        ''')
    o = '#last{height:3.33333px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


# PROGRAMMATIC

def test_variable_a():
    i = dedent('''
        x = #000000
        body
            color: x
        ''')
    o = 'body{color:#000000;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_variable_b():
    i = dedent('''
        x = 16px
        body
            border: x + 8px
        ''')
    o = 'body{border:24px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_mixin_decl_without_call():
    i = dedent('''
        mixin():
            width: 10px
            height: 20px
        .example
            width: 5px
        ''')
    o = '.example{width:5px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_mixin_a():
    i = dedent('''
        mixin():
            width: 10px
            height: 20px
        .example
            color: white
            mixin()
        ''')
    o = '.example{color:white;width:10px;height:20px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_mixin_b():
    i = dedent('''
        mixin(x y):
            width: x
            height: y
        .example
            mixin(5px 10px)
        ''')
    o = '.example{width:5px;height:10px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_mixin_c():
    i = dedent('''
        mixin(x y):
            width: x + 5
            height: y + 5
        .example
            mixin(5px 10px)
        ''')
    o = '.example{width:10px;height:15px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_mixin_variable_a():
    i = dedent('''
        mixin():
            width: 5px + x
        x = 20px
        .example
            mixin()
        ''')
    o = '.example{width:25px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_mixin_variable_b():
    i = dedent('''
        mixin(w v):
            width: w + v + x
        x = 20px
        .example
            mixin(30px 50px)
        ''')
    o = '.example{width:100px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


# TAGS

def test_flag_property_a():
    i = dedent('''
        .test
            (x) width: 50px
            (y) width: 20px
        (root.x)
        ''')
    o = '.test{width:50px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_property_b():
    i = dedent('''
        .test
            (x) width: 50px
            (y) width: 20px
        (root.y)
        ''')
    o = '.test{width:20px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_property_c():
    i = dedent('''
        .test
            (x) width: 50px
            (y) height: 20px
        (root.x)
        (root.y)
        ''')
    o = '.test{width:50px;}.test{height:20px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_property_d():
    i = dedent('''
        .testA
            (x) width: 50px
        .testB
            (y) height: 20px
        (root.x)
        (root.y)
        ''')
    o = '.testA{width:50px;}.testB{height:20px;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_property_e():
    i = dedent('''
        .test
            width: 20px
            (desktop) width: 50px
        (root)
        (root.desktop) "@media screen and (min-width:970px)"
        ''')
    o = '.test{width:20px;}@media screen and (min-width:970px){.test{width:50px;}}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_property_f():
    i = dedent('''
        .test
            color: #000000
            (x) color: #FFFFFF
        (root)
        (root.x) "@media screen and (min-width:970px)"
        ''')
    o = '.test{color:#000000;}@media screen and (min-width:970px){.test{color:#ffffff;}}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_block_a():
    i = dedent('''
        .test
            color: #000000
        (x) .test
            color: #FFFFFF
        ''')
    o = '.test{color:#000000;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_block_b():
    i = dedent('''
        .test
            color: #000000
        (x) .test
            color: #FFFFFE
        (root.x)
        ''')
    o = '.test{color:#fffffe;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_flag_block_c():
    i = dedent('''
        .test
            color: #000000
        (x) .test
            color: #FFFFFF
        (root)
        (root.x) "@media screen and (min-width:970px)"
        ''')
    o = '.test{color:#000000;}@media screen and (min-width:970px){.test{color:#ffffff;}}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_multilevel_definitions():
    i = dedent('''
        p
            width: 16px
            a
                color: red
        ''')
    o = 'p{width:16px;}p a{color:red;}'
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


### AT-RULES ###

def test_font_face():
    i = dedent('''
        @font-face
            font-family: Open Sans
            src: url("fonts/OpenSans-Regular-webfont.eot")
            font-weight: normal
            font-weight: 400
            font-style: normal
        .opensans
            font-family: Open Sans
        ''')
    o = ('@font-face{'
         'font-family:Open Sans;src:url(fonts/OpenSans-Regular-webfont.eot);'
         'font-weight:normal;font-weight:400;font-style:normal;}'
         '.opensans{font-family:Open Sans;}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_atrule_tag_a():
    i = dedent('''
        (d) @media screen and (min-width:970px)
            body
                width: 100%
        (root.d)
        ''')
    o = ('@media screen and (min-width:970px){body{width:100%;}}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_atrule_tag_b():
    i = dedent('''
        (d) @media screen and (min-width:970px)
            body
                width: 100%
        (root)
        ''')
    o = ''
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_atrule_tag_c():
    i = dedent('''
        (d) @media screen and (min-width:970px)
            body
                width: 100%
        (root.m)
        ''')
    o = ''
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_keyframe_a():
    i = dedent('''
        div
            width: 100px
            height: 100px
            background: red
            position: relative
            animation: warpmove 5s infinite
        @keyframes warpmove
            0%
                top: 0px
                background: red
                width: 100px
            100%
                top: 200px
                background: yellow
                width: 300px
        ''')
    o = ('div{width:100px;height:100px;background:red;position:relative;animation:warpmove 5s infinite;}'
         '@keyframes warpmove{0%{top:0px;background:red;width:100px;}'
         '100%{top:200px;background:yellow;width:300px;}}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_keyframe_b():
    i = dedent('''
        div
            width: 100px
            height: 100px
            background: red
            position: relative
            animation: warpmove 5s infinite
        @keyframes warpmove
            0%
                top: 0px
                background: red
                width: 100px
            (maybe) 50%
                top: 170px
                background: blue
                width: 50px
            100%
                top: 200px
                background: yellow
                width: 300px
        (root)
        ''')
    o = ('div{width:100px;height:100px;background:red;position:relative;animation:warpmove 5s infinite;}'
         '@keyframes warpmove{0%{top:0px;background:red;width:100px;}'
         '100%{top:200px;background:yellow;width:300px;}}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_keyframe_c():
    i = dedent('''
        div
            width: 100px
            height: 100px
            background: red
            position: relative
            animation: warpmove 5s infinite
        @keyframes warpmove
            (a) 0%
                top: 0px
                background: red
                width: 100px
            (b) 0%
                top: 170px
                background: blue
                width: 50px
            (a) 100%
                top: 200px
                background: yellow
                width: 300px
            (b) 100%
                top: 300px
                background: yellow
                width: 500px
        (root)
        (root.a)
        ''')
    o = ('div{width:100px;height:100px;background:red;position:relative;animation:warpmove 5s infinite;}'
         '@keyframes warpmove{0%{top:0px;background:red;width:100px;}'
         '100%{top:200px;background:yellow;width:300px;}}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_keyframe_d():
    i = dedent('''
        div
            width: 100px
            height: 100px
            background: red
            position: relative
            animation: warpmove 5s infinite
        @keyframes warpmove
            (a) 0%
                top: 0px
                background: red
                width: 100px
            (b) 0%
                top: 170px
                background: blue
                width: 50px
            (a) 100%
                top: 200px
                background: yellow
                width: 300px
            (b) 100%
                top: 300px
                background: yellow
                width: 500px
        (root)
        (root.b)
        ''')
    o = ('div{width:100px;height:100px;background:red;position:relative;animation:warpmove 5s infinite;}'
         '@keyframes warpmove{0%{top:170px;background:blue;width:50px;}'
         '100%{top:300px;background:yellow;width:500px;}}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o


def test_keyframe_e():
    i = dedent('''
        start = 0%
        end = 100%
        div
            width: 100px
            height: 100px
            background: red
            position: relative
            animation: warpmove 5s infinite
        @keyframes warpmove
            start
                top: 0px
                background: red
                width: 100px
            end
                top: 200px
                background: yellow
                width: 300px
        ''')
    o = ('div{width:100px;height:100px;background:red;position:relative;animation:warpmove 5s infinite;}'
         '@keyframes warpmove{0%{top:0px;background:red;width:100px;}'
         '100%{top:200px;background:yellow;width:300px;}}')
    ly = LY()
    ly.eval(i)
    assert ly.css() == o
