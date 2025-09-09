
class StringInvalidUnaryOperationSyntacticException(Exception):
    
    def __init__(self, current_token):
        error_message = f"Syntactic error in line {current_token.line_number}, column {current_token.first_char_index}. A string cannot be part of a unary operation." + f"\n[Error:{current_token.lexeme}|{current_token.line_number}]"
        super().__init__(error_message)