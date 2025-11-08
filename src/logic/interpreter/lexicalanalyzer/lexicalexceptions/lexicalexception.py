class LexicalException(Exception):
    DEBUG = False
    
    def __init__(self, error_message, lexeme, line_number, line, char_index):
        blanks = (char_index-1) * ' '
        error_message = error_message + f" At line {line_number}:" + f"\n{line}\n" + blanks
        if self.DEBUG:
            error_message += f"^\n[Error:{lexeme}|{line_number}]"
        super().__init__(error_message)
        self.lexeme = lexeme
        self.line_number = line_number
        self.line = line
        self.char_index = char_index
    
    @property
    def get_lexeme(self):
        return self.lexeme
    
    @property
    def get_line_number(self):
        return self.line_number
    
    @property
    def get_line(self):
        return self.line
    
    @property
    def get_char_index(self):
        return self.char_index