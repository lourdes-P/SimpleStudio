from logic.interpreter.lexicalanalizer.lexicalexceptions.lexicalexception import LexicalException

class LexicalExceptionInvalidSymbol(LexicalException):
    
    # throw con raise LexicalException("", "", int, "")
    def __init__(self, lexeme, line_number, line, char_index):
        super().__init__("Symbol " + lexeme + " is not a SimpleSem symbol.", lexeme, line_number, line, char_index)