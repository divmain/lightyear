from .globals import BLK_OPEN, BLK_CLOSE, COMMENT_OPEN, COMMENT_CLOSE


class LyError(Exception):
    def message(self):
        return "Error."

    def __repr__(self):
        return self.__class__.__name__ + ": " + self.message()

    def __str__(self):
        return self.__class__.__name__ + ": " + self.message()

    def return_code(self):
        return 1


class IndentError(LyError):
    pass


class UnknownMixinOrFunc(LyError):
    def __init__(self, *args, location=0):
        self.location = location
        super().__init__(*args)


class IncompatibleUnits(LyError):
    pass


class LySyntaxError(LyError):
    def __init__(self, pos, text):
        self.clean_text(pos, text)
        self.get_line_info()

    def clean_text(self, pos, text):
        removals = [(x, len(x)) for x in (BLK_OPEN, BLK_CLOSE, COMMENT_OPEN, COMMENT_CLOSE)]

        for removal, rlength in removals:
            count = text.count(removal, 0, pos)
            pos -= count * rlength
            text = text.replace(removal, '')

        self.pos = pos
        self.text = text

    def get_line_info(self):
        self.line_no = self.text.count('\n', 0, self.pos)
        start_line = self.text.rfind('\n', 0, self.pos) + 1
        end_line = self.text.find('\n', self.pos)
        if end_line == -1:
            end_line = len(self.text)
        self.line_text = self.text[start_line:end_line]
        self.pos_on_line = self.pos - start_line

        if start_line == 0:
            self.pre_context = None
        else:
            end_line_before = start_line - 1
            start_line_before = self.text.rfind('\n', 0, end_line_before) + 1
            self.pre_context = self.text[start_line_before:end_line_before]

        if end_line == len(self.text):
            self.post_content = None
        else:
            start_line_after = end_line + 1
            end_line_after = self.text.find('\n', start_line_after)
            self.post_context = self.text[start_line_after:end_line_after]

    def message(self):
        return 'Syntax error in section starting on line {}.'.format(
            self.line_no+1)
