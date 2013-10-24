import re
from collections import OrderedDict

from parsimonious.grammar import Grammar

from .errors import IndentationError
from .globals import BLK_OPEN, BLK_CLOSE, INDENT_SIZE, COMMENT_DELIM
from .types import RuleBlock, UnpackMe, RootBlock, IgnoreMe, ParentReference

ly_grammar = ""
funcmap = {}
defer_children_eval = []


### GRAMMAR HANDLING ###

class GDef(object):
    '''
    Decorator for defining LightYear syntax.
    '''
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
                    defer_children_eval.append(name)

    def __call__(self, f):
        for name in self.rulenames:
            funcmap[name] = f


### LIGHTYEAR PARSER ###

class LY(object):
    '''
    Parses LightYear code and generates CSS as output.
    '''
    grammar = None

    def __init__(self, env=None, debug=False):
        if not self.grammar:
            self.__class__.grammar = Grammar(ly_grammar)['ltree']
        self.env = env or {}
        self.debug = debug

    def eval(self, ly_code):
        '''
        Accept a string containing LightYear code as input, and recursively
        evaluate the root node.
        '''
        ly_code = '\n'.join(tokenize_whitespace(ly_code))
        self.debug = DebugGenerator(ly_code) if self.debug else False

        node = self.grammar.parse(ly_code)
        self.ltree = self._evalnode(node)
        self.flatten()

    def _evalnode(self, node):
        '''
        Evaluate a Parsimonious node.
        '''
        fn = funcmap.get(node.expr_name, lambda env, node, children: children)
        if node.expr_name in defer_children_eval:
            return fn(self.env, node)
        children = [self._evalnode(child) for child in node]

        # Mixins return lists that need to be unpacked.
        for i, child in enumerate(children):
            if isinstance(child, UnpackMe):
                for packed_child in reversed(child):
                    children.insert(i+1, packed_child)

        return fn(self.env, node, children)

    def flatten(self):
        '''
        Flatten all nested rules and convert parent references
        to standard selectors.  Execute only after LightYear
        code evaluation.
        '''
        for i, element in enumerate(self.ltree):
            if isinstance(element, RuleBlock):
                for j, child_element in reversed(list(enumerate(element.block))):
                    # Move nested RuleBlock objects to ltree and modify selectors.
                    if isinstance(child_element, RuleBlock):
                        child_element.selectors = element.selectors + child_element.selectors
                        self.ltree.insert(i+1, child_element)
                        element.block[j] = IgnoreMe()

                    # Find parent selectors and convert to standard RuleBlocks.
                    elif isinstance(child_element, ParentReference):
                        ps_rule_block = child_element.rule_block
                        if len(ps_rule_block.selectors) > 1:
                            new_selectors = (
                                child_element.selectors[:-1] +
                                [child_element.selectors[-1] + ps_rule_block.selectors[0]] +
                                ps_rule_block.selectors[1:]
                                )
                        else:
                            new_selectors = (
                                element.selectors[:-1] +
                                [element.selectors[-1] + ps_rule_block.selectors[0]]
                                )
                        new_block = RuleBlock(
                            tag=ps_rule_block.tag,
                            selectors=new_selectors,
                            block=ps_rule_block.block,
                            index=ps_rule_block.index)
                        self.ltree.insert(i+1, new_block)

                        element.block[j] = IgnoreMe()

    def reduce(self):
        '''
        Consolidate rules with identical selectors into single rules.
        '''

        # Reduce blocks.
        ltree_reduced = OrderedDict()
        non_block_count = 0
        for element in self.ltree:
            if hasattr(element, 'selectors'):
                hash_ = repr(element.selectors)
            elif hasattr(element, 'text'):
                hash_ = element.text
            else:
                hash_ = non_block_count
                non_block_count += 1

            if hasattr(element, 'block'):
                if hash_ in ltree_reduced:
                    ltree_reduced[hash_].block += element.block
                else:
                    ltree_reduced[hash_] = element

            else:
                ltree_reduced[hash_] = element

        ltree_reduced = [ltree_reduced[k] for k in ltree_reduced]

        # Reduce properties.
        for element in ltree_reduced:
            non_property_count = 0
            if hasattr(element, 'block'):
                block_reduced = OrderedDict()
                for child in element.block:
                    if hasattr(child, 'prop'):
                        block_reduced[child.prop] = child
                    else:
                        block_reduced[non_property_count] = child
                        non_property_count += 1
                element.block = [block_reduced[k] for k in block_reduced]

        self.ltree = ltree_reduced

    def css(self):
        '''
        Output minified CSS.  Should not be run until LightYear code is
        evaluated and the resulting structure flattened.
        '''
        root_blocks = []
        for e in self.ltree:
            if isinstance(e, RootBlock):
                root_blocks.append(e)
        if not root_blocks:
            root_blocks.append(RootBlock(tag_name=None, prefix=''))

        output = ''
        for root_block in root_blocks:
            output += root_block.prefix
            if root_block.prefix:
                output += '{'
            output += ''.join(e.css(tag=root_block.tag_name, debug=self.debug)
                              if hasattr(e, 'css')
                              else ''
                              for e in self.ltree)
            if root_block.prefix:
                output += '}'

        return output

    def pretty_css(self):
        '''
        Output prettified CSS.
        '''
        css_chars = list(self.css())

        # Insert spaces and newlines.
        skip = False
        for i, c in enumerate(css_chars):
            this_two = ''.join(css_chars[i:i+2]) if len(css_chars) > i+1 else None
            next_two = ''.join(css_chars[i+1:i+3]) if len(css_chars) > i+2 else None
            third = css_chars[i+2] if len(css_chars) > i+2 else None

            if c == ';' and not next_two == '/*':
                css_chars.insert(i+1, '\n')
            elif this_two == '/*':
                if skip:
                    skip = False
                    continue
                css_chars.insert(i, ' ')
                skip = True
            elif c == ':':
                css_chars.insert(i+1, ' ')
            elif c == '{':
                if skip:
                    skip = False
                    continue
                css_chars.insert(i+1, '\n')
                css_chars.insert(i, ' ')
                skip = True
            elif c == '}':
                css_chars.insert(i+1, '\n')
            elif this_two == '*/' and not third == '{':
                css_chars.insert(i+2, '\n')

        # Insert Indentation
        dent = 0
        tab = '    '
        for i, c in enumerate(css_chars):
            next = css_chars[i+1] if len(css_chars) > i+1 else None

            if next == '}':
                dent -= 1
            if c == '{':
                dent += 1

            elif c == '\n':
                css_chars.insert(i+1, tab*dent)
                if next == '}':
                    dent += 1

        return ''.join(css_chars)


# Import LightYear grammar after LY class definition.
from . import lang


### PRE-PEG TOKENIZATION ###

def tokenize_whitespace(text):
    """
    For each line, indentify current level of indendation and compare
    against indentation of previous line.  Insert BLK_OPEN or BLK_CLOSE
    as appropriate.
    """

    firstline = True
    prevdent = 0

    lines = text.split('\n')

    for line in lines:
        line = line.expandtabs(INDENT_SIZE)

        # Don't allow empty lines to effect tracking of indentation.
        stripped = line.strip()
        if stripped == '' or stripped[:2] == '//':
            yield line
            continue

        # Check for indentation on the first line.
        if firstline:
            if line[0] == " ":
                raise IndentationError
            firstline = False

        leading_spaces = re.match('[ ]*', line).group()
        curdent = len(leading_spaces) // INDENT_SIZE

        if curdent == prevdent:
            yield line
        elif curdent == prevdent + 1:
            yield BLK_OPEN + line
        elif curdent < prevdent:
            yield BLK_CLOSE * (prevdent - curdent) + line
        else:
            raise IndentationError(line)

        prevdent = curdent

    # Handle indented last line.
    yield BLK_CLOSE * prevdent


def tokenize_comments(lines):
    '''
    Identify and tokenize comments.
    '''
    for line in lines:
        for possible in (x.start(0) for x in re.finditer('//', line)):
            if not _isquoted(line, possible):
                line = line[:possible] + COMMENT_DELIM + line[possible:] + COMMENT_DELIM
                break
        yield line


def _isquoted(line, pos):
    '''
    Return boolean value indicating whether the character at position
    pos resides within a quote.
    '''
    DQUO = False
    SQUO = False

    for i in range(0, pos):
        if not DQUO and not SQUO:
            if line[i] == '"':
                DQUO = True
            elif line[i] == "'":
                SQUO = True
        elif DQUO:
            if line[i] == '"':
                DQUO = False
        elif SQUO:
            if line[i] == "'":
                SQUO = False

    return (DQUO or SQUO)


### DEBUG ###

class DebugGenerator():
    def __init__(self, ly_code):
        self.ly_code = ly_code

    def line_number(self, index):
        return self.ly_code[:index].count('\n') + 1

    def line_number_comment(self, index):
        return '/*line{}*/'.format(self.line_number(index))

    def __nonzero__(self):
        return True
