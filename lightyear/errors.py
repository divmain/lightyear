class LyError(Exception):
    pass


class IndentationError(LyError):
    pass


class UnknownMixinOrFunc(LyError):
    def __init__(self, location):
        self.location = location
