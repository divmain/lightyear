ly_grammar = ""
funcmap = {}
defer_children_eval = []


class Grammar(object):
    def __init__(self, ruletxt, defer=False):
        global ly_grammar
        ly_grammar += ruletxt + '\n'

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
