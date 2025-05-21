class Token:

#json_data = json.dumps(token.__dict__) # para convertirlo fácil a json

    def __init__(self, token_name, lexeme, line_number):
        self._token_name = token_name
        self._lexeme = lexeme
        self._line_number = line_number
    
    @property
    def get_token_name(self):
        return self._token_name

    @property
    def get_lexeme(self):
        return self._lexeme

    @property
    def get_line_number(self):
        return self._line_number