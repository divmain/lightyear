class RuleBlock():
    def __init__(self, tag, selectors, block):
        self.tag = tag
        self.selectors = selectors
        self.block = block


class CSSRule():
    def __init__(self, tag, prop, values):
        self.tag = tag
        self.prop = prop
        self.values = values
