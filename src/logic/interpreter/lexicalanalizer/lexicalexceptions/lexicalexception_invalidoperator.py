from .lexicalexception import LexicalException

class LexicalExceptionInvalidOperator(LexicalException):
    # throw con raise LexicalException("", "", int, "")
    def __init__(self, lexeme, line_number, line):
        super.__init__(lexeme + " is not a SimpleSem operator.", lexeme, line_number, line)