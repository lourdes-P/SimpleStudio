class LexicalException(Exception):
    # throw con raise LexicalException("", "", int, "")
    def __init__(self, error_message, lexeme, line_number, line):
        super.__init__(error_message)
        self.lexeme = lexeme
        self.line_number = line_number
        self.line = line