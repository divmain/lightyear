from .globals import BLK_OPEN, BLK_CLOSE, COMMENT_DELIM


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


### Rules with no associated function.  Returns empty list.

Rule(r'''
'''.format(
    comment_delim=COMMENT_DELIM,
    blk_open=BLK_OPEN,
    blk_close=BLK_CLOSE))
