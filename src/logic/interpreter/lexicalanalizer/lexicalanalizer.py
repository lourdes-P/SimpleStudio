from iomanager.io_manager import IOManager
from interpreter.lexicalanalizer.reserved_word_manager.reserved_word_map import ReservedWordMap
from .token import Token
from lexicalexceptions.lexicalexception import LexicalException

class LexicalAnalizer:
    
    def __init__(self, io_manager, reserved_word_map):
        self.io_manager = io_manager
        self.reserved_word_map = reserved_word_map
        self.current_char = ''
        self.no_errors = True
        self.recover_from_error = False    # esto es por si se buscan varios errores léxicos
        # en una misma ejecución del léxico ( de una sola corrida; sigue el análisis)
        self.lexeme = ""
        self.update_current_char()

    def next_token(self):
        if(self.recover_from_error):
            self.update_char_to_next_blank()
            self.recover_from_error = False
        self.erase_lexeme()
        return self.s0()
    
    def erase_lexeme(self):
        self.lexeme = ""

    def update_lexeme(self):
        self.lexeme = self.lexeme + self.current_char

    def update_current_char(self):
        try:
            self.io_manager.get_next_char()
        except:
            print("Source Manager error.")
        
    def update_char_to_next_blank(self):
        while(not self.reachedEOF() and not self.current_char.isspace()):
            self.update_current_char()

    def s0(self):
        if(self.current_char.isspace()):
            self.update_current_char()
            return self.s0()
        elif (self.current_char == ','):
            self.update_lexeme()
            self.update_current_char()
            return self.s_comma()
        elif (self.current_char == '['):
            self.update_lexeme()
            self.update_current_char()
            return self.s_open_square_bracket()
        elif (self.current_char == ']'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_close_square_bracket()
        elif(self.current_char.isalpha()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_label_or_keyword()
        ## TODO
        else:
            self.update_lexeme()
            raise LexicalException(self.lexeme, self.io_manager.get_line_number, self.io_manager.get_current_line())

            


    def s_comma(self):
        return Token("comma", self.lexeme, self.io_manager.get_line_number)

    def s_open_square_bracket(self):
        return Token("open_square_bracket", self.lexeme, self.io_manager.get_line_number)

    def s_close_square_bracket(self):
        return Token("close_square_bracket", self.lexeme, self.io_manager.get_line_number)

    def s_label_or_keyword(self):
        if (self.current_char.isdigit()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_label()
        elif (self.current_char.isalpha()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_label_or_keyword()
        else:
            if(self.reserved_word_map.is_reserved_word(self.lexeme)):
                return Token(self.reserved_word_map.get_reserved_word_id(self.lexeme), self.lexeme, self.io_manager.get_line_number)
            else:
                return Token("label", self.lexeme, self.io_manager.get_line_number)
           

    def s_label(self):
        if (self.current_char.isalpha()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_label()
        else:
           return Token("label", self.lexeme, self.io_manager.get_line_number)



    def reachedEOF(self):
        return self.current_char == IOManager.EOF