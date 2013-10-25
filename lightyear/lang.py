import operator as op
from decimal import Decimal, getcontext
getcontext().prec = 6

from .globals import BLK_OPEN, BLK_CLOSE, COMMENT_OPEN, COMMENT_CLOSE
from .types import (RuleBlock, CSSRule, MixIn, UnpackMe, RootBlock,
                    Distance, ParentReference, Color, AtRuleBlock, Keyframe)
from .core import GDef
from .functions import builtin_funcs
from .errors import UnknownMixinOrFunc


@GDef(r'ltree = root_element+')
def ltree(env, node, children):
    return children


@GDef(r'root_element = ___ (root_block / at_rule / mixin_decl / var_decl / rule_block) ___')
def root_element(env, node, children):
    return children[1][0]


### SELECTORS ###

@GDef(r'rule_block = tag? simple_selector ("," _ simple_selector)* ___ block')
def rule_block(env, node, children):
    tag, simple_sel, more_selectors, _, block = children
    tag = tag[0] if tag else None

    selectors = [simple_sel]
    if more_selectors:
        selectors = selectors.extend([selector for _, selector in more_selectors])

    return RuleBlock(tag=tag,
                     selectors=selectors,
                     block=block,
                     index=node.start)


@GDef(r'block = blk_open ___ block_element+ blk_close')
def block(env, node, children):
    return children[2]


@GDef(r'block_element = (mixin_or_func_call / declaration / rule_block / parent_reference) ___')
def block_element(env, node, children):
    return children[0][0]


@GDef(r'simple_selector = selector_with_space? (((type_sel / universal_sel) (attribute_sel / id_class_sel / pseudo_class)*) / (attribute_sel / id_class_sel))')
def simple_selector(env, node, children):
    return node.text


@GDef(r'''
type_sel = name
universal_sel = "*"

attribute_sel = "[" name ("=" / "~=" / "|=") name "]"
id_class_sel = ("#" / ".") name

pseudo_class = ":" ((pseudo_class_param "(" num ")") / pseudo_class_noparam)
pseudo_class_param = "nth-child" / "nth-last-child" / "nth-of-type" / "nth-last-of-type" / "lang"
pseudo_class_noparam = "last-child" / "first-of-type" / "last-of-type" / "only-child" / "only-of-type" / "root" / "empty" / "target" / "enabled" / "disabled" / "checked" / "link" / "visited" / "hover" / "active" / "focus" / "first-letter" / "first-line" / "first-child" / "before" / "after"
''')
def selector_misc(env, node, children):
    return node.text


@GDef(r'selector_with_space = _? (">" / "+" / "~") _?')
def selector_with_space(env, node, children):
    'Support immediate child, immediate sibling, and general sibling selectors.'
    return node.text.strip()


### PARENT REFERENCE ###

@GDef(r'parent_reference = "&" parent_block')
def parent_reference(env, node, children):
    return ParentReference(children[1])


@GDef(r'parent_block = tag? (simple_selector / pseudo_class) ("," _ (simple_selector / pseudo_class))* ___ block')
def parent_block(env, node, children):
    tag, (simple_sel, ), more_selectors, _, block = children
    tag = tag[0] if tag else None

    selectors = [simple_sel]
    if more_selectors:
        selectors = selectors.extend([selector for _, (selector, ) in more_selectors])

    return RuleBlock(tag=tag,
                     selectors=selectors,
                     block=block,
                     index=node.start)


### AT-RULES ###

@GDef(r'at_rule = tag? "@" (at_rule_keyframe / at_rule_normal)')
def at_rule(env, node, children):
    tag = children[0][0] if children[0] else None
    text, block = children[2][0]

    return AtRuleBlock(tag=tag,
                       text=text.strip(),
                       block=block,
                       index=node.start)


@GDef(r'at_rule_normal = any ___ block')
def at_rule_normal(env, node, children):
    text, _, block = children
    return (text, block)


@GDef(r'at_rule_keyframe = "keyframes" _ name ___ keyframes_block')
def at_rule_keyframes(env, node, children):
    _, _, name, ___, block = children
    return ("keyframes " + name, block)


@GDef(r'keyframes_block = blk_open ___ keyframe+ blk_close')
def keyframes_block(env, node, children):
    return children[2]


@GDef(r'keyframe = tag? expr ___ block ___')
def keyframe(env, node, children):
    tag, condition, _, block, _ = children
    tag = tag[0] if tag else None
    return Keyframe(
        tag=tag,
        condition=condition,
        block=block,
        index=node.start)


### CSS RULES ###

@GDef(r'declaration = tag? property ":" _ expr+')
def declaration(env, node, children):
    tag, prop, _, _, values = children
    tag = tag[0] if tag else None
    return CSSRule(tag=tag,
                   prop=prop,
                   values=values,
                   index=node.start)


@GDef(r'property = ~"[a-zA-Z\_\-][a-zA-Z0-9\-\_]*"')
def property_(env, node, children):
    return node.text


@GDef(r'expr = (mixin_or_func_call / math / color / string_val) _?')
def expr(env, node, children):
    return children[0][0]


### MIXINS, FUNCTIONS, and VARIABLES ###

@GDef(r'mixin_decl = name "(" (_? name _?)* "):" ___ block',
      defer=True)
def mixin_decl(env, node):
    name, _, variables, _, _, block = node

    ly_engine = LY(env=env)
    name = ly_engine._evalnode(name)
    variables = [varname for _, varname, _ in ly_engine._evalnode(variables)]

    def f(*args):
        global_vars = list(env.items())
        local_vars = list(zip(variables, args))
        temp_env = dict(global_vars + local_vars)

        ly_engine_local = LY(env=temp_env)
        return ly_engine_local._evalnode(block)

    env[name] = MixIn(name=name, func=f)


@GDef(r'mixin_or_func_call = tag? name "(" (_? expr _?)* ")"')
def mixin_or_func_call(env, node, children):
    tag, name, _, args, _ = children
    tag = tag[0] if tag else None
    args = [arg for _, arg, _ in args]

    if name in builtin_funcs:
        return_val = builtin_funcs[name](env, *args)
    elif name in env:
        return_val = UnpackMe(env[name](*args))
    else:
        raise UnknownMixinOrFunc(
            'Unknown mixin or function: {}'.format(name),
            location=node.start)

    if isinstance(return_val, UnpackMe) and tag:
        for element in return_val:
            if hasattr(element, tag):
                element.tag = tag
    return return_val


@GDef(r'lvalue = ~"[a-zA-Z\_\-][a-zA-Z0-9\-\_]*"')
def lvalue(env, node, children):
    if node.text in env:
        return env[node.text]
    return node.text


@GDef(r'var_decl = name _? "=" _? expr ___')
def var_decl(env, node, children):
    name, _, _, _, value, _ = children
    env[name] = value


### ROOT BLOCKS ###

@GDef(r'root_block = "(root" ("." name)? ")" _? string_val?')
def root_block(env, node, children):
    _, possible_name, _, _, prefix = children
    tag_name = possible_name[0][1] if possible_name else None
    if not prefix:
        prefix = ''
    else:
        prefix = prefix[0]
    return RootBlock(tag_name=tag_name, prefix=prefix)


### TEXT ###

@GDef(r'''string_val = ~'\"[^"\n]*\"' ''')
def string_val(env, node, children):
    return node.text[1:-1]


### NUMERIC ###

@GDef(r'math = sum')
def math(env, node, children):
    return children[0]


@GDef(r'''
sum = prod (_? sum_op _? prod)*
prod = equality (_ prod_op _ equality)*
equality = value (_ equality_op _ value)*
''')
def math_operation(env, node, children):
    if len(children[1]):
        operations = [
            (operator, operand) for _, operator, _, operand in children[1]]
        return do_math(children[0], operations)
    return children[0]


@GDef(r'''
sum_op = "+" / "-"
prod_op = "*" / "/"
equality_op = "=="
''')
def operator_symbols(env, node, children):
    return node.text


@GDef(r'value = num_val / lvalue / paren')
def math_value(env, node, children):
    return children[0]


@GDef(r'paren = "(" _? sum _? ")"')
def math_paren(env, node, children):
    return children[2]


@GDef(r'num_val = distance / num / hexcolor / color_name / lvalue')
def num_val(env, node, children):
    return children[0]


@GDef(r'distance = num unit')
def distance(env, node, children):
    num, unit = children
    return Distance(value=num, unit=unit)


@GDef(r'num = ~"\-?\d+(\.\d+)?"')
def num(env, node, children):
    return Decimal(node.text)


@GDef(r'unit = "em" / "ex" / "px" / "cm" / "mm" / "in" / "pt" / "pc" / "deg" / "rad" / "grad" / "ms" / "s" / "hz" / "khz" / "%"')
def unit(env, node, children):
    return node.text


### MATH HELPER FUNCTION ###

OPERATORS = {'+': op.add,
             '-': op.sub,
             '*': op.mul,
             '/': op.truediv,
             '==': op.eq
             }


def do_math(start, operations):
    output_val = start
    for optr_symbol, operand in operations:
        output_val = OPERATORS[optr_symbol](output_val, operand)
    return output_val


### COLORS ###

@GDef(r'color = color_name / hexcolor')
def color(env, node, children):
    return node.text


@GDef(r'hexcolor = "#" ~"[0-9a-fA-F]+"')
def color_(env, node, children):
    return Color(node.text, ctype='hex')


@GDef(r'color_name = "aliceblue" / "antiquewhite" / "aqua" / "aquamarine" / "azure" / "beige" / "bisque" / "black" / "blanchedalmond" / "blue" / "blueviolet" / "brown" / "burlywood" / "cadetblue" / "chartreuse" / "chocolate" / "coral" / "cornflowerblue" / "cornsilk" / "crimson" / "cyan" / "darkblue" / "darkcyan" / "darkgoldenrod" / "darkgray" / "darkgreen" / "darkkhaki" / "darkmagenta" / "darkolivegreen" / "darkorange" / "darkorchid" / "darkred" / "darksalmon" / "darkseagreen" / "darkslateblue" / "darkslategray" / "darkturquoise" / "darkviolet" / "deeppink" / "deepskyblue" / "dimgray" / "dodgerblue" / "firebrick" / "floralwhite" / "forestgreen" / "fuchsia" / "gainsboro" / "ghostwhite" / "gold" / "goldenrod" / "gray" / "green" / "greenyellow" / "honeydew" / "hotpink" / "indianred " / "indigo " / "ivory" / "khaki" / "lavender" / "lavenderblush" / "lawngreen" / "lemonchiffon" / "lightblue" / "lightcoral" / "lightcyan" / "lightgoldenrodyellow" / "lightgray" / "lightgreen" / "lightpink" / "lightsalmon" / "lightseagreen" / "lightskyblue" / "lightslategray" / "lightsteelblue" / "lightyellow" / "lime" / "limegreen" / "linen" / "magenta" / "maroon" / "mediumaquamarine" / "mediumblue" / "mediumorchid" / "mediumpurple" / "mediumseagreen" / "mediumslateblue" / "mediumspringgreen" / "mediumturquoise" / "mediumvioletred" / "midnightblue" / "mintcream" / "mistyrose" / "moccasin" / "navajowhite" / "navy" / "oldlace" / "olive" / "olivedrab" / "orange" / "orangered" / "orchid" / "palegoldenrod" / "palegreen" / "paleturquoise" / "palevioletred" / "papayawhip" / "peachpuff" / "peru" / "pink" / "plum" / "powderblue" / "purple" / "red" / "rosybrown" / "royalblue" / "saddlebrown" / "salmon" / "sandybrown" / "seagreen" / "seashell" / "sienna" / "silver" / "skyblue" / "slateblue" / "slategray" / "snow" / "springgreen" / "steelblue" / "tan" / "teal" / "thistle" / "tomato" / "turquoise" / "violet" / "wheat" / "white" / "whitesmoke" / "yellow" / "yellowgreen"')
def color_name(env, node, children):
    return Color(node.text, ctype='named')


### BASIC ###

@GDef(r'tag = "(" name ")" _')
def tag(env, node, children):
    return children[1]


@GDef(r'name = ~"[a-zA-Z\_\-][a-zA-Z0-9\-\_]*"')
def name(env, node, children):
    return node.text


@GDef(r'any = ~".+"')
def any(env, node, children):
    return node.text.strip()


@GDef(r'''
___ = ~"[\s]*" (comment ~"[\s]*")*
_ = ~"[ \t]+"
blk_open = "{blk_open}"
blk_close = "{blk_close}"
comment = ~"{comment_open}.*(?!{comment_close})"
'''.format(
    comment_open=COMMENT_OPEN,
    comment_close=COMMENT_CLOSE,
    blk_open=BLK_OPEN,
    blk_close=BLK_CLOSE)
)
def return_none(env, node, children):
    return None


from .core import LY
