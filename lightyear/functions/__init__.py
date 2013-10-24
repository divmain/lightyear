builtin_funcs = {}


### HELPER FUNCTIONS ###

def bifunc(f):
    'Decorator to build builtin_funcs dict.'
    builtin_funcs[f.__name__] = f


### BUILT-IN LIGHTYEAR FUNCTIONS ###

from . import colors
from . import functional_notation
from . import grid
