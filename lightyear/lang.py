from .globals import BLK_OPEN, BLK_CLOSE, COMMENT_DELIM
from .types import RuleBlock


rules = ""
funcmap = {}
defer_children_eval = []


class Rule(object):
    def __init__(self, ruletxt, defer=False):
        global rules
        rules += ruletxt + '\n'

        self.rulenames = []
        for line in ruletxt.split('\n'):
            line = line.strip()
            if line:
                name = line.split('=')[0].strip()
                self.rulenames.append(name)
                if defer:
                    defer_children_eval.append(self.rulename)

    def __call__(self, f):
        for name in self.rulenames:
            funcmap[name] = f


###

@Rule(r'ltree = root_element*')
def ltree(env, node, children):
    return children


@Rule(r'root_block / mixin_decl / var_decl / rule_block / (___ nl ___)')
def root_element(env, node, children):
    return children[0]


### SELECTORS

@Rule(r'rule_block = tag? simple_selector ("," _ simple_selector)* ___ nl ___ block')
def rule_block(env, node, children):
    tag, simple_sel, more_selectors, _, _, _, block = children

    selectors = [simple_sel]
    if more_selectors:
        selectors = selectors.extend([selector for _, selector in more_selectors])

    return RuleBlock(tag=tag,
                     selectors=selectors,
                     block=block)


@Rule(r'block = blk_open (declaration / rule_block / parent_selector / nl)+ blk_close')
def block(env, node, children):
    return children[1]


Rule(r'parent_selector = "&" rule_block')


@Rule(r'simple_selector = (type_sel / universal_sel) (attribute_sel / id_sel / pseudo_class)*')
def simple_selector(env, node, children):
    return node.text

Rule(r'''
type_sel = name
universal_sel = "*"

attribute_sel = "[" name ("=" / "~=" / "|=") name "]"
id_sel = "#" name

pseudo_class = ":" (pseudo_class_param "(" num ")") / pseudo_class_not / pseudo_class_noparam
pseudo_class_param = "nth-child" / "nth-last-child" / "nth-of-type" / "nth-last-of-type" / "lang"
pseudo_class_noparam = "last-child" / "first-of-type" / "last-of-type" / "only-child" / "only-of-type" / "root" / "empty" / "target" / "enabled" / "disabled" / "checked" / "link" / "visited" / "hover" / "active" / "focus" / "first-letter" / "first-line" / "first-child" / "before" / "after"
pseudo_class_not = "not(" ... ")"
''')


### Rules with no associated function.  Returns empty list.

Rule(r'''
tag = "(" name ")" _
num = ~"\-?\d+(\.\d+)?"
hex = ~"[0-9a-fA-F]+/"
hexcolor = "#" hex
name = ~"[a-zA-Z\_][a-zA-Z0-9\-\_]*"

unit = "em" / "ex" / "px" / "cm" / "mm" / "in" / "pt" / "pc" / "deg" / "rad" / "grad" / "ms" / "s" / "hz" / "khz" / "%"
color_name = "aliceblue" / "antiquewhite" / "aqua" / "aquamarine" / "azure" / "beige" / "bisque" / "black" / "blanchedalmond" / "blue" / "blueviolet" / "brown" / "burlywood" / "cadetblue" / "chartreuse" / "chocolate" / "coral" / "cornflowerblue" / "cornsilk" / "crimson" / "cyan" / "darkblue" / "darkcyan" / "darkgoldenrod" / "darkgray" / "darkgreen" / "darkkhaki" / "darkmagenta" / "darkolivegreen" / "darkorange" / "darkorchid" / "darkred" / "darksalmon" / "darkseagreen" / "darkslateblue" / "darkslategray" / "darkturquoise" / "darkviolet" / "deeppink" / "deepskyblue" / "dimgray" / "dodgerblue" / "firebrick" / "floralwhite" / "forestgreen" / "fuchsia" / "gainsboro" / "ghostwhite" / "gold" / "goldenrod" / "gray" / "green" / "greenyellow" / "honeydew" / "hotpink" / "indianred " / "indigo " / "ivory" / "khaki" / "lavender" / "lavenderblush" / "lawngreen" / "lemonchiffon" / "lightblue" / "lightcoral" / "lightcyan" / "lightgoldenrodyellow" / "lightgray" / "lightgreen" / "lightpink" / "lightsalmon" / "lightseagreen" / "lightskyblue" / "lightslategray" / "lightsteelblue" / "lightyellow" / "lime" / "limegreen" / "linen" / "magenta" / "maroon" / "mediumaquamarine" / "mediumblue" / "mediumorchid" / "mediumpurple" / "mediumseagreen" / "mediumslateblue" / "mediumspringgreen" / "mediumturquoise" / "mediumvioletred" / "midnightblue" / "mintcream" / "mistyrose" / "moccasin" / "navajowhite" / "navy" / "oldlace" / "olive" / "olivedrab" / "orange" / "orangered" / "orchid" / "palegoldenrod" / "palegreen" / "paleturquoise" / "palevioletred" / "papayawhip" / "peachpuff" / "peru" / "pink" / "plum" / "powderblue" / "purple" / "red" / "rosybrown" / "royalblue" / "saddlebrown" / "salmon" / "sandybrown" / "seagreen" / "seashell" / "sienna" / "silver" / "skyblue" / "slateblue" / "slategray" / "snow" / "springgreen" / "steelblue" / "tan" / "teal" / "thistle" / "tomato" / "turquoise" / "violet" / "wheat" / "white" / "whitesmoke" / "yellow" / "yellowgreen"
nl = "\n"

blk_open = "{blk_open}"
blk_close = "{blk_close}"
comment = ~"{comment_delim}[^{comment_delim}]*{comment_delim}"

any = ~"."
___ = ~"\s*" (comment ~"\s*")?
_ = ~"\s+"
'''.format(
    comment_delim=COMMENT_DELIM,
    blk_open=BLK_OPEN,
    blk_close=BLK_CLOSE))
