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


### Rules with no associated function.  Returns empty list.

Rule(r'''
'''.format(
    comment_delim=COMMENT_DELIM,
    blk_open=BLK_OPEN,
    blk_close=BLK_CLOSE))
