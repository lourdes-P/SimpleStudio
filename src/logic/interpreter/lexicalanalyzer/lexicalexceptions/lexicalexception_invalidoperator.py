from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException

class LexicalExceptionInvalidOperator(LexicalException):
    
    # throw con raise LexicalException("", "", int, "")
    def __init__(self, lexeme, line_number, line, char_index):
        error_message = f"{lexeme} is not a SimpleSem operator."
        super().__init__(error_message, lexeme, line_number, line, char_index)