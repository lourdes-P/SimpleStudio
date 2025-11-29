class Token:

    def __init__(self, token_name, lexeme, line_number, first_char_index):
        self._token_name = token_name
        self._lexeme = lexeme
        self._line_number = line_number
        self._first_char_index = first_char_index
    
    @property
    def token_name(self):
        return self._token_name

    @property
    def lexeme(self):
        return self._lexeme

    @property
    def line_number(self):
        return self._line_number
    
    @property
    def first_char_index(self):
        return self._first_char_index