from reserved_word_manager.reserved_word_map import ReservedWordMap
from iomanager import IOManager
from token import Token
from lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator

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
            self.current_char = self.io_manager.get_next_char()
        except:
            print("Source Manager error.")
        
    def update_char_to_next_blank(self):
        while(not self.reachedEOF() and not self.current_char.isspace()):
            self.update_current_char()

    def s0(self):
        if (self.current_char.isspace()):
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
        elif (self.current_char.isalpha()):            
            self.update_lexeme()
            self.update_current_char()
            return self.s_identifier_or_keyword()       
        elif (self.current_char.isdigit()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_int() 
        elif (self.current_char == '('):
            self.update_lexeme()
            self.update_current_char()
            return self.s_open_parenthesis()
        elif (self.current_char == ')'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_open_parenthesis()
        elif (self.current_char == '+'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_plus()
        elif (self.current_char == '-'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_minus()
        elif (self.current_char == '@'):            
            self.update_current_char()
            return self.s_annotation()
        elif (self.current_char == '*'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_multiplication()
        elif (self.current_char == '/'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_division()
        elif (self.current_char == '&'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_and()
        elif (self.current_char == '|'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_or()
        elif (self.current_char == '='):
            self.update_lexeme()
            self.update_current_char()
            return self.s_equals()
        elif (self.current_char == '>'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_greater()
        elif (self.current_char == '<'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_lesser()
        elif (self.current_char == '!'):
            self.update_lexeme()
            self.update_current_char()
            return self.s_not()
        elif (self.current_char == IOManager.EOF):
            return self.s_eof()
        else:
            self.update_lexeme()
            raise LexicalExceptionInvalidSymbol(self.lexeme, self.io_manager.get_line_number, self.io_manager.get_current_line())
          

    def s_comma(self):
        return Token("comma", self.lexeme, self.io_manager.get_line_number)

    def s_open_square_bracket(self):
        return Token("open_square_bracket", self.lexeme, self.io_manager.get_line_number)

    def s_close_square_bracket(self):
        return Token("close_square_bracket", self.lexeme, self.io_manager.get_line_number)

    def s_identifier_or_keyword(self):
        if (self.current_char.isdigit()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_identifier()
        elif (self.current_char.isalpha()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_identifier_or_keyword()
        else:
            if(self.reserved_word_map.is_reserved_word(self.lexeme)):
                return Token(self.reserved_word_map.get_reserved_word_id(self.lexeme), self.lexeme, self.io_manager.get_line_number)
            else:
                return Token("identifier", self.lexeme, self.io_manager.get_line_number)
           
    def s_identifier(self):
        if (self.current_char.isalpha() or self.current_char.isdigit()):
            self.update_lexeme()
            self.update_current_char()
            return self.s_identifier()
        else:
           return Token("identifier", self.lexeme, self.io_manager.get_line_number)

    def s_int(self):
        if (self.current_char.isdigit()):            
            self.update_lexeme()
            self.update_current_char()
            return self.s_int()
        else:
            return Token("int", self.lexeme, self.io_manager.get_line_number)

    def s_open_parenthesis(self):
        return Token("open_parenthesis", self.lexeme, self.io_manager.get_line_number)

    def s_close_parenthesis(self):
        return Token("close_parenthesis", self.lexeme, self.io_manager.get_line_number)

    def s_plus(self):
        return Token("plus", self.lexeme, self.io_manager.get_line_number)

    def s_minus(self):
        return Token("minus", self.lexeme, self.io_manager.get_line_number)
    
    def s_annotation(self):
        if (self.is_enter(self.current_char) or self.reachedEOF()):                        
            self.update_current_char()
            return self.s0()
        else:            
            self.update_current_char()
            return self.s_annotation()        
    
    def s_multiplication(self):
        return Token("multiplication", self.lexeme, self.io_manager.get_line_number)

    def s_division(self):
        return Token("division", self.lexeme, self.io_manager.get_line_number)

    def s_and(self):
        return Token("and", self.lexeme, self.io_manager.get_line_number)

    def s_or(self):
        return Token("or", self.lexeme, self.io_manager.get_line_number)
    
    def s_equals(self):
        if (self.current_char == '='):
            self.update_lexeme()
            self.update_current_char()            
            return Token("equals", self.lexeme, self.io_manager.get_line_number)            
        else:
            # no actualizo el lexema, debería?
            raise LexicalExceptionInvalidOperator(self.lexeme, self.io_manager.get_line_number, self.io_manager.get_current_line())

    def s_greater(self):
        if (self.current_char == '='):
            self.update_lexeme()
            self.update_current_char()
            return self.s_greater_or_equal()
        else:
            return Token("greater", self.lexeme, self.io_manager.get_line_number)
            
    def s_greater_or_equal(self):
        return Token("greater_or_equal", self.lexeme, self.io_manager.get_line_number)        

    def s_lesser(self):
        if (self.current_char == '='):
            self.update_lexeme()
            self.update_current_char()
            return self.s_lesser_or_equal()
        else:
            return Token("lesser", self.lexeme, self.io_manager.get_line_number)

    def s_lesser_or_equal(self):
        return Token("lesser_or_equal", self.lexeme, self.io_manager.get_line_number)        

    def s_not(self):
        if (self.current_char == '='):
            self.update_lexeme()
            self.update_current_char()
            return self.s_different()
        else:
            return Token("not", self.lexeme, self.io_manager.get_line_number)

    def s_different(self):
        return Token("different", self.lexeme, self.io_manager.get_line_number)                

    def s_eof(self):
        return Token("EOF", "", self.io_manager.get_line_number)

    def reachedEOF(self):
        return self.current_char == IOManager.EOF
    
    def is_enter(self, char):
        return char == IOManager.END_OF_LINE