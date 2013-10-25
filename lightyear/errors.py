class LyError(Exception):
    pass


class IndentationError(LyError):
    pass


class UnknownMixinOrFunc(LyError):
    def __init__(self, *args, location=0):
        self.location = location
        super().__init__(*args)


class IncompatibleUnits(LyError):
    pass
